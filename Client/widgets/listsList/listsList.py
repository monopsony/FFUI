from .listsListBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
import pandas as pd
from Events import EventWidgetClass
from widgets.pandaTable.pandaTable import pandaTable
from widgets.listPeek.listPeek import listPeek
from widgets.other.tables import listInfoTable, listListingsTable, listCraftTable
from widgets.other.confirmWidgets import (
    listListingsConfirmWidget,
    listCraftConfirmWidget,
)
import logging

logger = logging.getLogger(__name__)


class listsList(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)
        self.subscribeToEvents()
        self.setupUi(self)

        ## REPLACE PLACEHOLDER ITEM LIST TABLE
        listsListTable = pandaTable(
            launcher,
            filterKey="Name",
            eventName="LISTSLISTTABLE",
            cellHeight=33,
            configKey="listsListTable",
            isMenu=True,
        )
        self.leftLayout.replaceWidget(self.listsListTablePlaceholder, listsListTable)
        self.listsListTablePlaceholder.hide()
        self.listsListTable = listsListTable

        ## REPLACE PLACEHOLDER lists PEEK
        peek = listPeek(self.launcher)
        self.rightLayout.replaceWidget(self.listPeekPlaceholder, peek)
        self.listPeek = peek

        # INFO
        self.fillInfoTab()

        # LISTINGS
        self.fillListingsTab()

        # CRAFT
        self.fillCraftTab()

        # FLIP
        self.fillFlipTab()

    model = None

    def fillInfoTab(self):
        layout = self.infoLayout

        tbl = listInfoTable(self.launcher)
        layout.addWidget(tbl)

    def fillListingsTab(self):
        layout = self.listingsLayout

        confirm = listListingsConfirmWidget(self.launcher)
        layout.addWidget(confirm)

        listingsTable = listListingsTable(self.launcher)
        layout.addWidget(listingsTable)

    def fillCraftTab(self):
        layout = self.craftLayout

        confirm = listCraftConfirmWidget(self.launcher)
        layout.addWidget(confirm)

        craftTable = listCraftTable(self.launcher)
        layout.addWidget(craftTable)

    def fillFlipTab(self):
        pass

    def subscribeToEvents(self):
        self.eventSubscribe("LISTSLISTTABLE_DATA_SELECTED", self.applyListSelection)
        self.eventSubscribe("CLIENT_LISTS_LOADED", self.displayLists)
        self.eventSubscribe("CLIENT_LIST_LOADED", self.displayLists)
        self.eventSubscribe("CLIENT_MBINFO_UPDATE", self.updateSelection)

    def displayLists(self, *args):
        # self.setItems(self.launcher.client.items[["NameKey", "Name", "Icon"]])
        lists = self.launcher.client.lists
        nameData = [{"Name": x} for x in lists.keys()]
        df = pd.DataFrame(nameData)
        self.listsListTable.setData(df, cols=["Name"], base=True)

    selectedList = None

    def applyListSelection(self, lst, col=0):
        logger.debug(f"applying list selection: {lst['Name']}")
        self.selectedList = lst
        client = self.launcher.client

        # update list of items (only once, items dont change after all)
        if lst.get("ItemListCache", None) is None:
            lst = client.lists[lst["Name"]]
            df = client.items
            df = df[df["ItemId"].isin(lst["ItemIds"])]
            df.reset_index(drop=True, inplace=True)
            lst["ItemListCache"] = df

        # update market board info (as a copy) - needs to be updated
        info = client.mbGetListInfo(lst["ItemListCache"], allQualities=True)
        lst["ItemInfoCache"] = info  # is None if not all item infos are present

        self.eventPush("LISTSLIST_LIST_SELECTED", lst, col)

    def updateSelection(self, *args):
        logger.debug(
            f'listsList received CLIENT_MBINFO_UPDATE; updating selection {((self.selectedList is not None) and self.selectedList["Name"]) or None}'
        )
        if self.selectedList is None:
            return
        self.applyListSelection(self.selectedList)
