import pandas as pd
import numpy as np
import logging, traceback, os
from .Metrics import ACTIVE_METRICS

logger = logging.getLogger(__name__)

# giving mbInfo these columns by default avoids errors when the first item
# searched doesnt exist on market board as well as other things
# need to keep updating this if more columns are added further down the line

DEFAULT_COLUMNS = [
    "Name",
    "Quality",
    "averagePrice",
    "averagePriceHQ",
    "averagePriceNQ",
    "craftPrice",
    "flipPriceNQ",
    "flipPriceHQ",
    "currentAveragePrice",
    "currentAveragePriceHQ",
    "currentAveragePriceNQ",
    "salesPerDayHQ",
    "itemID",
    "lastUploadTime",
    "listings",
    "blacklisted",
    "maxPrice",
    "maxPriceHQ",
    "maxPriceNQ",
    "minPrice",
    "minPriceHQ",
    "minPriceNQ",
    "salesPerDayNQ",
    "recentHistory",
    "salesPerDay",
    "stackSizeHistogram",
    "stackSizeHistogramHQ",
    "stackSizeHistogramNQ",
    "worldID",
    "NameKey",
] + list(ACTIVE_METRICS["INFO"].keys())


class MBInfo:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventSubscribe("CLIENT_MBINFO_REQUEST", self.fetchMBInfo)
        self.eventSubscribe("CLIENT_MBCRAFT_REQUEST", self.fetchCraftPrice)
        self.eventSubscribe("CLIENT_MBFLIP_REQUEST", self.fetchFlipPrice)
        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.saveMBInfoCache)

    mbInfo = pd.DataFrame({}, columns=DEFAULT_COLUMNS.copy())

    def mbItemsWorldsPrepare(self, items, worlds):
        if type(items) != list:
            items = [items]

        if worlds is None:
            worlds = [self.getConfig("world")] * len(items)
        elif type(worlds) != list:
            worlds = [worlds] * len(items)

        # remove duplicates
        itemsUnique, worldsUnique = [], []
        alreadySeen = []
        for i in range(len(items)):
            key = self.mbItemWorldKey(items[i], worlds[i])
            if key in alreadySeen:
                continue
            alreadySeen.append(key)
            itemsUnique.append(items[i])
            worldsUnique.append(worlds[i])

        return itemsUnique, worldsUnique

    def getBlacklisted(self, listingsList):
        blRetainers = self.getConfig("retainerBlacklist")
        if blRetainers is None:
            return np.nan
        for x in listingsList:
            retName = x["retainerName"]
            if retName in blRetainers:
                return f"Retainer: {retName}"
        return np.nan

    def getAlreadyListed(self, itemId):
        listings = self.getConfig("currentListings")
        if listings is None:
            return np.nan
        if itemId in listings:
            return "Already listed"
        return np.nan

    def fetchMBInfo(self, items, worlds=None, quiet=False):
        if type(items) == pd.DataFrame:
            seriesList = []
            for _, item in items.iterrows():
                seriesList.append(item)
            items = seriesList

        items, worlds = self.mbItemsWorldsPrepare(items, worlds)
        ids = [x["ItemId"] for x in items]
        names = [x["Name"] for x in items]
        icons = [x["Icon"] for x in items]
        nameKey = [x["NameKey"] for x in items]
        index = [self.mbItemWorldKey(x, world) for x, world in zip(items, worlds)]
        logger.debug(f"Fetching MB info for: {index}")

        d = self.gatherUniversalisQueries(zip(ids, worlds))
        d = pd.DataFrame(d, index=index, columns=DEFAULT_COLUMNS)

        # add additional columns
        d["Name"] = names
        d["Icon"] = icons
        d["NameKey"] = nameKey
        d["ItemId"] = ids

        # check the blacklist
        retainerBL = d["listings"].map(self.getBlacklisted, na_action="ignore")
        listedBL = d["ItemId"].map(self.getAlreadyListed, na_action="ignore")
        listedBL.update(retainerBL)
        d["blacklisted"] = listedBL

        ## Add seperate HQ and NQ
        dhq, dnq = d.copy(), d.copy()
        indexHQ = [
            self.mbItemWorldKey(x, world, hq=True) for x, world in zip(items, worlds)
        ]
        indexNQ = [
            self.mbItemWorldKey(x, world, hq=False) for x, world in zip(items, worlds)
        ]
        for col in d.columns:
            if type(col) != str:
                continue
            if col.endswith("HQ"):
                colBase = col.replace("HQ", "")
                dhq[colBase] = d[col]
            if col.endswith("NQ"):
                colBase = col.replace("NQ", "")
                dnq[colBase] = d[col]
        dhq.index = indexHQ
        dnq.index = indexNQ

        # add quality thingy
        d["Quality"] = "Any"
        dhq["Quality"] = "HQ"
        dnq["Quality"] = "NQ"

        d = pd.concat([d, dhq, dnq])
        # custom metrics
        self.setProgress(
            currentProgress=0,
            currentMax=0,
            progressText=f"Calculating custom info metrics",
        )
        metrics = ACTIVE_METRICS["INFO"]
        for k, v in metrics.items():
            self.setProgress(
                currentProgress=0,
                currentMax=0,
                progressText=f"Calculating custom metric {k}",
            )
            try:
                d[k] = v(d)
                logger.info(f"Successfully calculated metric: {k}")
            except Exception as e:
                d[k] = np.nan
                logger.error(f"Failed to compute metric {k}: {e}")
                logger.error(f"{traceback.format_exc()}")

        # better method, no old reference destroying
        self.mbInfo = self.mbInfo.combine_first(
            d
        )  # adds non-existing rows (updates nans too)
        self.mbInfo.update(d)  # updates all existing values from d into mbInfo
        logger.debug(f"In fetchMBInfo: mbInfo now contains {len(d)} elements")
        if not quiet:
            self.eventPush("CLIENT_MBINFO_UPDATE")

    def hqTag(self, hq):
        if hq is None:
            return ""
        elif hq:
            return "HQ"
        else:
            return "NQ"

    def mbItemWorldKey(self, item, world=None, hq=None):
        if world is None:
            world = self.getConfig("world")

        if type(item) != int:
            item = item["ItemId"]

        hqTag = self.hqTag(hq)

        key = f"{item}{hqTag}__{world}"

        return key

    def mbGetListInfo(
        self, lst, world=None, allWorlds=False, hq=None, allQualities=False
    ):
        lstInfo = []
        for index, item in lst.iterrows():
            if not self.hasItemInfo(item):
                return None
            if allQualities:
                lstInfo.append(self.mbGetItemInfo(item, hq=None))
                lstInfo.append(self.mbGetItemInfo(item, hq=False))
                lstInfo.append(self.mbGetItemInfo(item, hq=True))
            else:
                lstInfo.append(self.mbGetItemInfo(item, hq=hq))

        df = pd.DataFrame(lstInfo)
        return df

    def mbGetItemInfo(self, item, world=None, allWorlds=False, hq=None):

        if allWorlds:
            if not self.hasItemInfo(item, allWorlds=True):
                self.eventPush("CLIENT_MBFLIP_REQUEST", item)
                return None

            cWorlds = self.getConfig("connectedWorlds") + [self.getConfig("world")]
            lst = []
            for world in cWorlds:
                lst.append(self.mbGetItemInfo(item, world=world, hq=hq))

            return pd.DataFrame(lst, index=cWorlds)

        key = self.mbItemWorldKey(item, world, hq=hq)

        if self.hasItemInfo(item, world):
            return self.mbInfo.loc[key]
        else:
            logger.error(
                f"In mbGetItemInfo, hasItemInfo of {item['Name']} was None. Request sent to try to fix the problem."
            )
            self.eventPush("CLIENT_MBINFO_REQUEST", item)
            return None

    def hasItemInfo(self, item, world=None, allWorlds=False):
        if allWorlds:
            cWorlds = self.getConfig("connectedWorlds")
            hasItem = [self.hasItemInfo(item, world=x) for x in cWorlds]
            return all(hasItem)

        tup = self.mbItemWorldKey(item, world)
        return tup in self.mbInfo.index

    def fetchMBInfoComps(self, items, world=None, **kwargs):
        compsAll = self.getRecipeComp(items, asItem=True)
        compsAll += items
        compsNew = [x for x in compsAll if not self.hasItemInfo(x)]

        if len(compsNew) == 0:
            return
        compsNew, worlds = self.mbItemsWorldsPrepare(compsNew, world)

        self.fetchMBInfo(compsNew, worlds, **kwargs)

    def fetchCraftPrice(self, items, world=None, **kwargs):
        if type(items) == pd.DataFrame:
            seriesList = []
            for _, item in items.iterrows():
                seriesList.append(item)
            items = seriesList

        items, worlds = self.mbItemsWorldsPrepare(items, world)

        self.fetchMBInfoComps(items, world=world, quiet=True, **kwargs)
        # self.mbGetCraftPrice(items)

        self.setProgress(
            currentProgress=0,
            currentMax=len(items),
            progressText=f"Calculating craft price",
        )
        for item in items:
            for hq in [None, True, False]:
                key = self.mbItemWorldKey(item, world, hq)
                if np.isnan(self.mbInfo.loc[key, "craftPrice"]):
                    self.mbInfo.loc[key, "craftPrice"] = self.mbGetCraftPrice(
                        item, world=world
                    )
            self.currentProgress += 1
            self.setProgress()

        keys = [self.mbItemWorldKey(item, world, None) for item in items]
        keys += [self.mbItemWorldKey(item, world, True) for item in items]
        keys += [self.mbItemWorldKey(item, world, False) for item in items]

        # custom metrics
        self.setProgress(
            currentProgress=0,
            currentMax=0,
            progressText=f"Calculating custom craft metrics",
        )
        metrics = ACTIVE_METRICS["CRAFT"]
        for k, v in metrics.items():
            self.setProgress(
                currentProgress=0,
                currentMax=0,
                progressText=f"Calculating custom metric {k}",
            )
            try:
                self.mbInfo.loc[keys, k] = v(self.mbInfo.loc[keys])
                logger.info(f"Successfully calculated metric: {k}")
            except Exception as e:
                self.mbInfo.loc[keys, k] = np.nan
                logger.error(f"Failed to compute metric {k}: {e}")
                logger.error(f"{traceback.format_exc()}")

        self.eventPush("CLIENT_MBINFO_UPDATE")

    def mbGetCraftPrice(self, item, world=None):
        if world is None:
            world = self.getConfig("world")

        key = self.mbItemWorldKey(item, world)
        if not np.isnan(self.mbInfo.loc[key, "craftPrice"]):
            return self.mbInfo.loc[key, "craftPrice"]

        craftPrice = 0
        comps = self.getRecipeComp(item, shallow=True)
        recipe = self.getRecipe(item)
        if recipe is None:
            craftPrice = np.inf
        else:
            for compId, amount in comps.items():
                compItem = self.getItem(id=compId)
                compInfo = self.mbGetItemInfo(compItem)
                craftPrice += (
                    min(compInfo["minPrice"], self.mbGetCraftPrice(compItem)) * amount
                )
            craftPrice /= recipe["AmountResult"]

        if np.isnan(craftPrice):
            craftPrice = np.inf
        self.mbInfo.loc[key, "craftPrice"] = craftPrice
        return craftPrice

    def mbGetFlipPrice(self, item, world=None, hq=False):
        if world is None:
            world = self.getConfig("world")

        cWorlds = self.getConfig("connectedWorlds")

        if True:
            return None

        tag = "HQ" if hq else "NQ"
        key = self.mbItemWorldKey(item, world)
        if not np.isnan(self.mbInfo.loc[key, "flipPrice" + tag]):
            return self.mbInfo.loc[key, "flipPrice" + tag]

        flipPrice = 0
        # TBA

        self.mbInfo.loc[key, "flipPrice" + tag] = flipPrice
        return craftPrice

    def fetchFlipPrice(self, items, world=None):
        if type(items) == pd.DataFrame:
            seriesList = []
            for _, item in items.iterrows():
                seriesList.append(item)
            items = seriesList

        items, worlds = self.mbItemsWorldsPrepare(items, world)

        cWorlds = self.getConfig("connectedWorlds") + [self.getConfig("world")]

        allItems, allWorlds = [], []
        for x in items:
            for world in cWorlds:
                if not self.hasItemInfo(x, world=world):
                    allItems.append(x)
                    allWorlds.append(world)

        self.fetchMBInfo(allItems, allWorlds, quiet=True)

        for item in items:
            minNQ, minHQ = np.inf, np.inf
            self.mbGetFlipPrice(item)

            # if np.isnan(self.mbInfo.loc[key, "flipPrice"]):
            #     self.mbInfo.loc[key, "flipPrice"] = self.mbGetCraftPrice(
            #         item, world=world
            #     )

        self.eventPush("CLIENT_MBINFO_UPDATE")

    nLastSaved = 0

    def saveMBInfoCache(self):
        N = len(self.mbInfo)
        if (
            N - self.nLastSaved < 50
        ):  # save only when at least 50 new items are there (arbitrary)
            return
        self.setProgress(
            progressText="Saving current MBInfo to cache",
            currentMax=0,
            currentProgress=0,
        )
        logger.info(f"Saved current MBInfo to cache ({len(self.mbInfo)} items)")
        mbInfoPath = os.path.join("Cache", "mbInfoC.csv")

        self.mbInfo.to_csv(mbInfoPath)
