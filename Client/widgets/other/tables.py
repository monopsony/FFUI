from widgets.pandaTable.pandaTable import pandaTable
import pandas as pd
import numpy as np

from Client.Metrics import ACTIVE_METRICS


class itemInfoTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="ITEMINFOTABLE",
            verticalHeader=True,
            cellHeight=25,
            **kwargs
        )

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.updateSelectedItem)

    def updateSelectedItem(self, item, col):
        self.setData(item)


class itemCraftTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="ITEMCRAFTTABLE",
            verticalHeader=True,
            cellHeight=25,
            **kwargs
        )

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.updateSelectedItem)
        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    selectedItem = None

    def updateSelectedItem(self, item, col):
        self.selectedItem = item
        self.refresh()

    def refresh(self):
        if self.selectedItem is None:
            self.setEmpty()
            return

        client = self.launcher.client

        if not client.hasItemInfo(self.selectedItem):
            self.setEmpty()
            return

        info = client.mbGetItemInfo(self.selectedItem)
        if np.isnan(info["craftPrice"]):
            self.setEmpty()
            return

        cols = [
            "craftPrice",
            "currentAveragePrice",
            "currentAveragePriceNQ",
            "currentAveragePriceHQ",
            "regularSaleVelocity",
            "nqSaleVelocity",
            "hqSaleVelocity",
            "averagePrice",
            "averagePriceNQ",
            "averagePriceHQ",
            "minPrice",
            "minPriceNQ",
            "minPriceHQ",
            "maxPrice",
            "maxPriceNQ",
            "maxPriceHQ",
        ]
        cols += list(ACTIVE_METRICS["CRAFT"].keys())
        self.setData(
            info,
            cols=cols,
        )


class itemlistingsTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="ITEMLISTINGSTABLE",
            horizontalHeader=True,
            cellHeight=25,
            **kwargs
        )

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.updateSelectedItem)
        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    selectedItem = None

    def updateSelectedItem(self, item, col):
        self.selectedItem = item
        self.refresh()

    def refresh(self):
        if self.selectedItem is None:
            self.setEmpty()
            return

        client = self.launcher.client

        if not client.hasItemInfo(self.selectedItem):
            self.setEmpty()
            return

        info = client.mbGetItemInfo(self.selectedItem)
        listings = info["listings"]
        if (type(listings) != list) and (np.isnan(listings)):
            self.setEmpty()
            return

        listings = pd.DataFrame(listings)
        self.setData(
            listings,
            cols=["quantity", "pricePerUnit", "hq", "retainerName", "total"],
        )


class itemFlipTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="ITEMFLIPTABLE",
            verticalHeader=True,
            horizontalHeader=True,
            cellHeight=25,
            **kwargs
        )

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.updateSelectedItem)
        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    selectedItem = None

    def updateSelectedItem(self, item, col):
        self.selectedItem = item
        self.refresh()

    def refresh(self):
        if self.selectedItem is None:
            self.setEmpty()
            return

        client = self.launcher.client

        if not client.hasItemInfo(self.selectedItem, allWorlds=True):
            self.setEmpty()
            return

        info = client.mbGetItemInfo(self.selectedItem, allWorlds=True)
        print(info)
        # if np.isnan(info["flipPrice"]):
        #     self.setEmpty()
        #     return

        self.setData(
            info,
            cols=[
                "minPrice",
                "minPriceNQ",
                "minPriceHQ",
                "averagePrice",
                "averagePriceNQ",
                "averagePriceHQ",
            ],
        )


class listInfoTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="LISTINFOTABLE",
            filterKey="NameKey",
            horizontalHeader=True,
            cellHeight=25,
            iconApplicationCol=0,
            iconDataCol="Icon",
            multiSelect=True,
            **kwargs
        )

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.updateSelectedList)

    def updateSelectedList(self, selected, col):
        df = selected["ItemListCache"]
        self.setData(df, cols=["Name", "ItemId", "Craftable", "CraftType"], base=True)


class listListingsTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="LISTLISTINGSTABLE",
            filterKey="NameKey",
            horizontalHeader=True,
            cellHeight=30,
            iconApplicationCol=0,
            iconDataCol="Icon",
            **kwargs
        )

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.updateSelectedList)
        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    selectedList = None

    def updateSelectedList(self, lst, col):
        self.selectedList = lst
        self.refresh()

    def refresh(self):
        if self.selectedList is None:
            self.setEmpty()
            return

        client = self.launcher.client
        lst = self.selectedList
        info = lst["ItemInfoCache"]

        if info is None:
            self.setEmpty()
            return

        self.setData(
            info,
            cols=[
                "Name",
                "averagePriceNQ",
                "averagePriceHQ",
                "minPriceNQ",
                "minPriceHQ",
                "nqSaleVelocity",
                "hqSaleVelocity",
            ],
            base=True,
        )


class listCraftTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="LISTCRAFTTABLE",
            filterKey="NameKey",
            horizontalHeader=True,
            cellHeight=30,
            iconApplicationCol=0,
            iconDataCol="Icon",
            **kwargs
        )

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.updateSelectedList)
        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    selectedList = None

    def updateSelectedList(self, lst, col):
        self.selectedList = lst
        self.refresh()

    def refresh(self):
        if self.selectedList is None:
            self.setEmpty()
            return

        client = self.launcher.client
        lst = self.selectedList
        info = lst["ItemInfoCache"]

        if info is None:
            self.setEmpty()
            return

        if info["craftPrice"].isna().values.any():
            self.setEmpty()
            return

        cols = [
            "Name",
            "Quality",
            "craftPrice",
            "averagePriceNQ",
            "averagePriceHQ",
            "minPriceNQ",
            "minPriceHQ",
            "nqSaleVelocity",
            "hqSaleVelocity",
        ]
        cols += list(ACTIVE_METRICS["CRAFT"].keys())
        self.setData(
            info,
            cols=cols,
            base=True,
        )
