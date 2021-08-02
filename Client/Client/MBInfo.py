import pandas as pd
import numpy as np

# giving mbInfo these columns by default avoids errors when the first item
# searched doesnt exist on market board as well as other things
# need to keep updating this if more columns are added further down the line
DEFAULT_COLUMNS = [
    "averagePrice",
    "averagePriceHQ",
    "averagePriceNQ",
    "craftPrice",
    "flipPriceNQ",
    "flipPriceHQ",
    "currentAveragePrice",
    "currentAveragePriceHQ",
    "currentAveragePriceNQ",
    "hqSaleVelocity",
    "itemID",
    "lastUploadTime",
    "listings",
    "maxPrice",
    "maxPriceHQ",
    "maxPriceNQ",
    "minPrice",
    "minPriceHQ",
    "minPriceNQ",
    "nqSaleVelocity",
    "recentHistory",
    "regularSaleVelocity",
    "stackSizeHistogram",
    "stackSizeHistogramHQ",
    "stackSizeHistogramNQ",
    "worldID",
]


class MBInfo:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventSubscribe("CLIENT_MBINFO_REQUEST", self.fetchMBInfo)
        self.eventSubscribe("CLIENT_MBCRAFT_REQUEST", self.fetchCraftPrice)
        self.eventSubscribe("CLIENT_MBFLIP_REQUEST", self.fetchFlipPrice)

    mbInfo = pd.DataFrame({}, columns=DEFAULT_COLUMNS.copy())

    def mbItemsWorldsPrepare(self, items, worlds):
        if type(items) != list:
            items = [items]

        if worlds is None:
            worlds = [self.getPara("world")] * len(items)
        elif type(worlds) != list:
            worlds = [worlds] * len(items)

        return items, worlds

    def fetchMBInfo(self, items, worlds=None):
        items, worlds = self.mbItemsWorldsPrepare(items, worlds)
        ids = [x["ItemId"] for x in items]
        index = [self.mbItemWorldKey(x, world) for x, world in zip(items, worlds)]

        d = self.gatherUniversalisQueries(zip(ids, worlds))
        d = pd.DataFrame(d, index=index)

        # remove old entries if existing
        # newIndices = set(d.index)
        # existingIndices = set(self.mbInfo.index)
        # removeIndices = newIndices.intersection(existingIndices)
        # mbInfo = self.mbInfo.drop(removeIndices)
        # self.mbInfo = mbInfo.append(d)

        # better method, no old reference destroying
        self.mbInfo = self.mbInfo.combine_first(
            d
        )  # adds non-existing rows (updates nans too)
        self.mbInfo.update(d)  # updates all existing values from d into mbInfo
        self.eventPush("CLIENT_MBINFO_UPDATE")

    def mbItemWorldKey(self, item, world=None):
        if world is None:
            world = self.getPara("world")

        if type(item) == int:
            key = f"{item}__{world}"
        else:
            key = f'{item["ItemId"]}__{world}'

        return key

    def mbGetItemInfo(self, item, world=None, allWorlds=False):

        if allWorlds:
            if not self.hasItemInfo(item, allWorlds=True):
                self.eventPush("CLIENT_MBFLIP_REQUEST", item)
                return None

            cWorlds = self.getPara("connectedWorlds") + [self.getPara("world")]
            lst = []
            for world in cWorlds:
                lst.append(self.mbGetItemInfo(item, world=world))

            return pd.DataFrame(lst, index=cWorlds)

        key = self.mbItemWorldKey(item, world)

        if self.hasItemInfo(item, world):
            return self.mbInfo.loc[key]
        else:
            self.eventPush("CLIENT_MBINFO_REQUEST", item)
            return None

    def hasItemInfo(self, item, world=None, allWorlds=False):
        if allWorlds:
            cWorlds = self.getPara("connectedWorlds")
            hasItem = [self.hasItemInfo(item, world=x) for x in cWorlds]
            return all(hasItem)

        tup = self.mbItemWorldKey(item, world)
        return tup in self.mbInfo.index

    def fetchMBInfoComps(self, items, world=None):
        compsAll = self.getRecipeComp(items, asItem=True)
        compsAll += items
        compsNew = [x for x in compsAll if not self.hasItemInfo(x)]

        if len(compsNew) == 0:
            return
        compsNew, worlds = self.mbItemsWorldsPrepare(compsNew, world)

        self.fetchMBInfo(compsNew, worlds)

    def fetchCraftPrice(self, items, world=None):
        items, worlds = self.mbItemsWorldsPrepare(items, world)

        self.fetchMBInfoComps(items, world=world)
        # self.mbGetCraftPrice(items)

        for item in items:
            key = self.mbItemWorldKey(item, world)
            # info = self.mbGetItemInfo(item)
            # info.loc["minPrice"] = 100
            if np.isnan(self.mbInfo.loc[key, "craftPrice"]):
                self.mbInfo.loc[key, "craftPrice"] = self.mbGetCraftPrice(
                    item, world=world
                )

        self.eventPush("CLIENT_MBINFO_UPDATE")

    def mbGetCraftPrice(self, item, world=None):
        if world is None:
            world = self.getPara("world")

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

        self.mbInfo.loc[key, "craftPrice"] = craftPrice
        return craftPrice

    def mbGetFlipPrice(self, item, world=None, hq=False):
        if world is None:
            world = self.getPara("world")

        cWorlds = self.getPara("connectedWorlds")

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
        items, worlds = self.mbItemsWorldsPrepare(items, world)

        cWorlds = self.getPara("connectedWorlds") + [self.getPara("world")]

        allItems, allWorlds = [], []
        for x in items:
            for world in cWorlds:
                if not self.hasItemInfo(x, world=world):
                    allItems.append(x)
                    allWorlds.append(world)

        self.fetchMBInfo(allItems, allWorlds)

        for item in items:
            minNQ, minHQ = np.inf, np.inf
            self.mbGetFlipPrice(item)

            # if np.isnan(self.mbInfo.loc[key, "flipPrice"]):
            #     self.mbInfo.loc[key, "flipPrice"] = self.mbGetCraftPrice(
            #         item, world=world
            #     )

        self.eventPush("CLIENT_MBINFO_UPDATE")
