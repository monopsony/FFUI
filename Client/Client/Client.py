from PyQt5.QtCore import QObject, QThread, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import time, os, glob, json
import pandas as pd
from Events import EventClass
import aiohttp, asyncio
from Client.Connector import Connector
from Client.MBInfo import MBInfo
from Client.Recipes import RecipeHandler

RECIPES_FILE = "Recipe.csv"
ITEMS_FILE = "Item.csv"
LISTS_DIR = "Lists"


def colsRemoveSpecialChars(df):
    df.columns = df.columns.str.replace("#", "ItemId")
    df.columns = df.columns.str.replace("[#,@,&,{,},\[,\], ,:]", "")
    return df


class Client(QObject, EventClass, Connector, MBInfo, RecipeHandler):
    def __init__(self, ui, *args, **kwargs):

        self.ui = ui
        super().__init__(*args, **kwargs)
        self.eventFree = "CLIENT_FREE"  # sends a CLIENT_FREE event whenever the client is done with something that occupied it
        self.eventBusy = "CLIENT_BUSY"

        # self.connector = Connector()

    def getItem(self, id=None, name=None):
        df = self.items

        if id is not None:
            item = df.loc[df["ItemId"] == id]
        elif name is not None:
            item = df.loc[df["NameKey"] == name.lower()]
        else:
            print(f"Get item called but no id or name given")

        if len(item) == 0:
            return None
        elif len(item) == 1:
            return item.iloc[0]
        else:
            print(
                f"More than one item found under id/name {id}/{name}, using first found",
            )
            print(item)
            return item.iloc[0]

    csvData = {}

    def loadDataCSV(self):

        for path in glob.glob(os.path.join("data", "*.csv")):
            name = os.path.basename(path).replace(".csv", "")
            self.csvData[name] = pd.read_csv(path)

    def loadItems(self):
        if not os.path.exists(ITEMS_FILE):
            print(f'No file found under {ITEMS_FILE}. Fetch them using "item update"')
            return

        r = pd.read_csv(ITEMS_FILE)
        r = colsRemoveSpecialChars(r)
        r.insert(1, "NameKey", r["Name"].str.lower(), True)
        r = r[~(r["Name"].isnull())]

        self.items = r
        self.items.sort_values("Name", inplace=True, ignore_index=True)
        print(f"Loaded a total of {len(self.items)} items")
        self.eventPush("CLIENT_ITEMS_LAODED")

    def loadRecipes(self):
        if not os.path.exists(RECIPES_FILE):
            print(
                f'No file found under {RECIPES_FILE}. Fetch them using "recipe update"'
            )
            return

        r = pd.read_csv(RECIPES_FILE)
        r = colsRemoveSpecialChars(r)
        # r.insert(1, "NameKey", r["Name"].str.lower(), True)
        # r = r[~(r["Name"].isnull())]

        self.recipes = r
        # self.recipes.sort_values("Name", inplace=True, ignore_index=True)
        print(f"Loaded a total of {len(self.recipes)} RECIPES")
        self.eventPush("CLIENT_RECIPES_LAODED")

    def run(self):
        self.loadParas()
        self.loadDataCSV()
        self.loadItems()
        self.loadRecipes()

        while True:
            time.sleep(0.1)
            self.eventHandle()

    # PARAS
    def loadParas(self):
        with open("para.json", "r") as f:
            p = json.load(f)

        self.para = p

    def getPara(self, key):
        return self.para.get(key, None)

    def setPara(self, key, value):
        self.para[key] = value
        self.eventPush("CLIENT_PARA_SET", key, value)

    def saveParas(self):
        with open("para.json", "w") as f:
            f.write(json.dumps(self.para, indent=2, sort_keys=True))

    ## UTILS
    def getIconPath(self, icon_id):
        dir2 = str(icon_id // 1000 * 1000).zfill(6)
        png = str(icon_id).zfill(6) + ".png"

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

    # elif command == "recipe":

    #     c = Client()
    #     item = self.getItem(id=sys.argv[2])
    #     print(c.getRecipeComp(item))

    # a = asyncio.run(c.universalis_query("Shiva", "5510"))
    # print(a)
