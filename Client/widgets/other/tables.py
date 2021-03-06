from widgets.pandaTable.pandaTable import pandaTable
import pandas as pd
import numpy as np
from PyQt5 import QtWidgets
from numbers import Number
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
            "blacklisted",
        ]
        cols += list(ACTIVE_METRICS["CRAFT"].keys())
        self.setData(info, cols=cols, base=True)

    def baseConfigPath(self):
        return ["tables", "itemCraftTable"]


class qpItemCraftTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="QUICKPREVIEWITEMCRAFTTABLE",
            verticalHeader=True,
            cellHeight=25,
            **kwargs,
        )

        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)
        self.tableView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )

    selectedItem = None

    def updateSelectedItem(self, item, col=0):
        self.selectedItem = item
        self.refresh()

    def refresh(self):
        if self.selectedItem is None:
            self.setEmpty()
            return

        client = self.launcher.client

        if not client.hasItemInfo(self.selectedItem):
            self.eventPush("CLIENT_MBCRAFT_REQUEST", self.selectedItem)
            self.setEmpty()
            return

        info = client.mbGetItemInfo(self.selectedItem)
        if np.isnan(info["craftPrice"]):
            self.setEmpty()
            return

        cols = [
            "craftPrice",
            "salesPerDay",
            "salesPerDayNQ",
            "salesPerDayHQ",
            "averagePrice",
            "averagePriceNQ",
            "averagePriceHQ",
            "minPrice",
            "minPriceNQ",
            "minPriceHQ",
        ]
        cols += list(ACTIVE_METRICS["CRAFT"].keys())
        self.setData(info, cols=cols, base=True)

    def baseConfigPath(self):
        return ["tables", "quickPreviewItemCraftTable"]


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
        if (type(listings) != list) or (type(listings) == float and np.isnan(listings)):
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


class qpItemFlipTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="QUICKPREVIEWITEMFLIPTABLE",
            verticalHeader=True,
            horizontalHeader=True,
            cellHeight=25,
            **kwargs,
        )

        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.refresh)

    selectedItem = None

    def updateSelectedItem(self, item, col=0):
        self.selectedItem = item
        self.refresh()

    def refresh(self):
        if self.selectedItem is None:
            self.setEmpty()
            return

        client = self.launcher.client

        if not client.hasItemInfo(self.selectedItem, allWorlds=True):
            self.eventPush("CLIENT_MBFLIP_REQUEST", self.selectedItem)
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
        return ["tables", "quickPreviewItemFlipTable"]


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
            "blacklisted",
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
            hasQuery=True,
            multiSelect=True,
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
            "blacklisted",
        ]
        cols += list(ACTIVE_METRICS["CRAFT"].keys())

        self.setData(
            info,
            cols=cols,
            base=True,
        )

    def getSelectedItems(self, filterBlacklisted=False):
        client = self.launcher.client
        selectedIndices = self.tableView.selectionModel().selectedIndexes()
        rows = [x.row() for x in selectedIndices]
        data = self.model._data
        itemSet = set()
        for row in rows:
            if filterBlacklisted:
                bl = data.loc[row, "blacklisted"]
                if (not isinstance(bl, Number)) or (not np.isnan(bl)):
                    continue
            itemName = data.at[data.index[row], "Name"]
            item = client.getItem(name=itemName)
            if item is None:
                logger.error(f"Found no item corresponding to name: {itemName}")
                continue
            itemId = item["ItemId"]
            itemSet.add(itemId)

        return itemSet

    def getTopItems(self, N, filterBlacklisted=False):
        client = self.launcher.client
        itemSet = set()
        data = self.model._data
        if filterBlacklisted:
            data = data[data["blacklisted"].isna()]
        for row in range(len(data)):
            itemName = data.at[data.index[row], "Name"]
            item = client.getItem(name=itemName)
            if item is None:
                logger.error(f"Found no item corresponding to name: {itemName}")
                continue
            itemId = item["ItemId"]
            itemSet.add(itemId)
            if len(itemSet) >= N:
                break

        return itemSet
