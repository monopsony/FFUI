from widgets.pandaTable.pandaTable import pandaTable
import pandas as pd
import numpy as np


class itemInfoTable(pandaTable):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            eventName="ITEMINFOTABLE",
            verticalHeader=True,
            cellHeight=25,
            **kwargs
        )

        self.eventSubscribe("ITEMLISTTABLE_DATA_SELECTED", self.updateSelectedItem)

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

        self.eventSubscribe("ITEMLISTTABLE_DATA_SELECTED", self.updateSelectedItem)
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

        self.setData(
            info,
            cols=[
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
            ],
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

        self.eventSubscribe("ITEMLISTTABLE_DATA_SELECTED", self.updateSelectedItem)
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

        self.eventSubscribe("ITEMLISTTABLE_DATA_SELECTED", self.updateSelectedItem)
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
