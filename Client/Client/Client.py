from PyQt5.QtCore import QObject, QThread, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import time, os, glob, json
import pandas as pd
import numpy as np
from Events import EventClass
import aiohttp, asyncio
from Client.Connector import Connector
from Client.MBInfo import MBInfo
from Client.Recipes import RecipeHandler
import logging
from collections import defaultdict
import webbrowser

logger = logging.getLogger(__name__)

ITEMS_FILE = "Item.csv"
ITEMS_COMBINED_FILE = "ItemsCombined.csv"
LISTS_DIR = "Lists"


def colsRemoveSpecialChars(df):
    df.columns = df.columns.str.replace("#", "ItemId")
    df.columns = df.columns.str.replace("[#,@,&,{,},\[,\], ,:]", "", regex=True)
    return df


class Client(QObject, EventClass, Connector, MBInfo, RecipeHandler):
    def __init__(self, ui, launcher, *args, **kwargs):

        self.ui = ui
        self.launcher = launcher
        super().__init__(*args, **kwargs)
        self.eventFree = "CLIENT_FREE"  # sends a CLIENT_FREE event whenever the client is done with something that occupied it
        self.eventBusy = "CLIENT_BUSY"

        self.subscribeToEvents()

        self.resetProgress()

    progressText = ""
    currentMax = 0
    currentProgress = 0

    def setProgress(self, progressText=None, currentMax=None, currentProgress=None):
        if progressText is None:
            progressText = self.progressText
        else:
            self.progressText = progressText

        if currentMax is None:
            currentMax = self.currentMax
        else:
            self.currentMax = currentMax

        if currentProgress is None:
            currentProgress = self.currentProgress
        else:
            self.currentProgress = currentProgress

        self.eventPush("CLIENT_PROGRESS", quiet=True)

    def resetProgress(self):
        self.progressText = ""
        self.currentMax = 0
        self.currentProgress = 0

    def subscribeToEvents(self):
        self.eventSubscribe("NEW_LIST_SAVED", self.loadList)
        self.eventSubscribe("CLIENT_FREE", self.resetProgress)

    def getItem(self, id=None, name=None):
        df = self.items

        if id is not None:
            item = df.loc[df["ItemId"] == id]
        elif name is not None:
            item = df.loc[df["NameKey"] == name.lower()]
        else:
            logger.warn(f"Get item called but no id or name given")

        if len(item) == 0:
            return None
            # return pd.Series({"ItemId": id, "Name": name, "Prohibited": True})
        elif len(item) == 1:
            return item.iloc[0]
        else:
            logger.warn(
                f"More than one item found under id/name {id}/{name}, using first found"
            )
            logger.warn(item)
            return item.iloc[0]

    def filteredItemList(self, iFilter, rFilter):
        items = self.items

    csvData = {}

    lists = {}

    def loadLists(self):
        if not os.path.exists("Lists"):
            os.mkdir("Lists")

        for path in glob.glob(os.path.join("Lists", "*.json")):
            self.loadList(path, quiet=True)

        self.eventPush("CLIENT_LISTS_LOADED")

    def loadList(self, path, quiet=False):
        if not os.path.exists:
            logger.error(f"Tried to load list at path {path}, but does not exist.")
            return

        name = os.path.basename(path).replace(".json", "")
        with open(path) as fil:
            data = json.load(fil)
        self.lists[name] = data
        data["Name"] = name
        data["Path"] = path
        data["ItemIds"] = list(set(data["ItemIds"]))

        if not quiet:
            self.eventPush("CLIENT_LIST_LOADED", name, path)

    def deleteList(self, lst):
        if type(lst) == str:
            lst = self.lists[lst]

        logger.info(f'Deleting list: {lst["Name"]}')
        os.remove(lst["Path"])
        del self.lists[lst["Name"]]
        self.eventPush("CLIENT_LISTS_LOADED")
        self.eventPush("LISTSLIST_LIST_SELECTED", None, None)

    def loadDataCSV(self):

        for path in glob.glob(os.path.join("data", "*.csv")):
            name = os.path.basename(path).replace(".csv", "")
            self.csvData[name] = pd.read_csv(path)

    def loadItems(self):
        if not os.path.exists(ITEMS_COMBINED_FILE):
            self.createItemRecipeCombined()

        self.items = pd.read_csv(ITEMS_COMBINED_FILE)
        self.eventPush("CLIENT_ITEMS_LOADED")
        logger.info(f"Loaded a total of {len(self.items)} items")

    currentlyLoadingCache = False

    def loadCache(self):
        self.currentLoadingCache = True
        if not os.path.exists("Cache"):
            os.mkdir("Cache")

        # MBINFO in cache
        mbInfoPath = os.path.join("Cache", "mbInfoC.csv")
        if os.path.exists(mbInfoPath):
            t = os.path.getmtime(mbInfoPath)
            dt = time.time() - t
            if dt <= 3600:
                self.promptLoadMBInfoCache(dt)

    def promptLoadMBInfoCache(self, dt):
        logger.info("Found recent MBInfo in cache")
        self.eventPush("ASK_LOAD_MBINFO_CACHE", dt)

    def createItemRecipeCombined(self):
        if not os.path.exists(ITEMS_FILE):
            logger.error(f"No file found under {ITEMS_FILE}. Help.")
            return

        logger.info(
            f"Creating combined Item/Recipe file, this might take a few minutes..."
        )

        r = pd.read_csv(ITEMS_FILE)
        r = colsRemoveSpecialChars(r)
        r.insert(1, "NameKey", r["Name"].str.lower(), True)
        r = r[~(r["Name"].isnull())]
        # r = r[r["IsUntradable"] == False]

        self.setProgress(
            progressText="Generating item-recipe list for the first time...",
            currentMax=len(r),
            currentProgress=0,
        )

        # update with recipes
        updateList, updateIndices = [], []
        for index, row in r.iterrows():
            rec = self.getRecipe(row)
            if rec is None:
                r.loc[index, ["Craftable"]] = False
            else:
                r.loc[index, ["Craftable"]] = True
                updateList.append(rec)
                updateIndices.append(index)
            self.setProgress(currentProgress=index)

        updateDF = pd.DataFrame(updateList, index=updateIndices)
        r = pd.concat([r, updateDF], axis=1)
        r.sort_values("Name", inplace=True, ignore_index=True)

        r.to_csv(ITEMS_COMBINED_FILE)

    def run(self):
        self.busy = True
        self.loadDataCSV()
        self.loadRecipes()
        self.loadItems()
        self.loadLists()
        self.loadCache()

        while True:
            time.sleep(0.1)
            self.eventHandle()

    def openBrowserTab(self, url):
        b = webbrowser.get()
        b.open_new_tab(url)

    def ffxivCraftItems(self, itemIds):
        url = "https://ffxivcrafting.com/list/saved/"

        itemStrings = [f"{x},1" for x in itemIds]
        url = url + ":".join(itemStrings)

        logger.info(f"Opening `{url}` in browser")
        self.openBrowserTab(url)
        self.eventPush("CRAFTING_ITEMS")

    # PARAS
    def getConfig(self, *args, **kwargs):
        return self.launcher.getConfig(*args, **kwargs)

    def setConfig(self, *args, **kwargs):
        return self.launcher.setConfig(*args, **kwargs)

    ## UTILS
    def getIconPath(self, iconId):
        iconId = int(iconId)
        dir2 = str(iconId // 1000 * 1000).zfill(6)
        png = str(iconId).zfill(6) + "_hr1.png"

        path = os.path.join("icon", dir2, png)
        return path


if __name__ == "__main__":

    command = sys.argv[1]

    if command == "connector":
        c = Connector()

        t = []
        for i in range(100):
            t.append(asyncio.ensure_future(c.universalis_query("Shiva", "5510")))

        a = c.gatherTasks(t, callback=c.printProgress)
        print("DONE", len(a))
