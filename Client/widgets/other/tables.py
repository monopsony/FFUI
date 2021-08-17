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
            **kwargs,
        )

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.updateSelectedItem)

    def updateSelectedItem(self, item, col):
        self.setData(item, base=True)

    def baseConfigPath(self):
        return ["tables", "itemInfoTable"]


class itemCraftTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="ITEMCRAFTTABLE",
            verticalHeader=True,
            cellHeight=25,
            **kwargs,
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
            "salesPerDay",
            "salesPerDayNQ",
            "salesPerDayHQ",
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
        self.setData(info, cols=cols, base=True)

    def baseConfigPath(self):
        return ["tables", "itemCraftTable"]


class itemListingsTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="itemListingsTable",
            horizontalHeader=True,
            cellHeight=25,
            **kwargs,
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
            base=True,
        )

    def baseConfigPath(self):
        return ["tables", "itemListingsTable"]


class itemFlipTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="ITEMFLIPTABLE",
            verticalHeader=True,
            horizontalHeader=True,
            cellHeight=25,
            **kwargs,
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
            base=True,
        )

    def baseConfigPath(self):
        return ["tables", "itemFlipTable"]


class genericListTable:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    listTableKey = "genericListTable"
    selectedList = None

    def baseConfigPath(self):
        if self.listTableKey == "genericListTable":
            logger.warn(
                f"In genericListTable: default listTableKey used. This should not be the case. Culprit: {type(self)}"
            )
        if self.selectedList is None:
            return ["tables", self.listTableKey]
        return ["tables", self.listTableKey, self.selectedList["Name"]]


class listInfoTable(genericListTable, pandaTable):
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
            **kwargs,
        )

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.updateSelectedList)

    listTableKey = "listInfoTable"

    def updateSelectedList(self, selected, col):
        self.selectedList = selected
        if selected is None:
            self.setEmpty()
            return

        df = selected["ItemListCache"]
        self.setData(df, cols=["Name", "ItemId", "Craftable", "CraftType"], base=True)


class listListingsTable(genericListTable, pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="LISTLISTINGSTABLE",
            filterKey="NameKey",
            horizontalHeader=True,
            cellHeight=30,
            iconApplicationCol=0,
            iconDataCol="Icon",
            **kwargs,
        )

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.updateSelectedList)
        # self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    listTableKey = "listListingsTable"

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

        cols = [
            "Name",
            "Quality",
            "averagePrice",
            "minPrice",
            "salesPerDay",
        ]
        cols += list(ACTIVE_METRICS["INFO"].keys())

        self.setData(
            info,
            cols=cols,
            base=True,
        )


class listCraftTable(genericListTable, pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="LISTCRAFTTABLE",
            filterKey="NameKey",
            horizontalHeader=True,
            cellHeight=30,
            iconApplicationCol=0,
            iconDataCol="Icon",
            **kwargs,
        )

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.updateSelectedList)
        # self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    listTableKey = "listCraftTable"

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
            "averagePrice",
            "minPrice",
            "salesPerDay",
        ]
        cols += list(ACTIVE_METRICS["CRAFT"].keys())

        self.setData(
            info,
            cols=cols,
            base=True,
        )
