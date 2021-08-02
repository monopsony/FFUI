from .itemListBase import Ui_Form
from widgets.itemPeek.itemPeek import itemPeek

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
import os, re
import pandas as pd
from Events import EventWidgetClass
from widgets.pandaTable.pandaTable import pandaTable
from widgets.other.tables import (
    itemInfoTable,
    itemCraftTable,
    itemlistingsTable,
    itemFlipTable,
)
from widgets.other.confirmWidgets import (
    itemCraftConfirmWidget,
    itemListingsConfirmWidget,
    itemFlipConfirmWidget,
)


class itemList(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)
        self.subscribeToEvents()
        self.setupUi(self)

        ## REPLACE PLACEHOLDER ITEM LIST TABLE
        # https://stackoverflow.com/questions/4625102/how-to-replace-a-widget-with-another-using-qt
        itemListTable = pandaTable(
            launcher,
            filterKey="NameKey",
            eventName="ITEMLISTTABLE",
            cellHeight=33,
            iconApplicationCol=0,
            iconDataCol="Icon",
        )
        self.leftLayout.replaceWidget(self.itemListTablePlaceholder, itemListTable)
        self.itemListTable = itemListTable

        ## REPLACE PLACEHOLDER ITEM PEEK
        peek = itemPeek(self.launcher)
        self.rightLayout.replaceWidget(self.itemPeekPlaceholder, peek)
        self.itemPeek = peek

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

        infoTable = itemInfoTable(self.launcher)
        layout.addWidget(infoTable)

    def fillListingsTab(self):
        layout = self.listingsLayout

        confirm = itemListingsConfirmWidget(self.launcher)
        layout.addWidget(confirm)

        listingsTable = itemlistingsTable(self.launcher)
        layout.addWidget(listingsTable)

    def fillCraftTab(self):

        layout = self.craftLayout

        confirm = itemCraftConfirmWidget(self.launcher)
        layout.addWidget(confirm)

        craftTable = itemCraftTable(self.launcher)
        layout.addWidget(craftTable)

    def fillFlipTab(self):

        layout = self.flipLayout

        confirm = itemFlipConfirmWidget(self.launcher)
        layout.addWidget(confirm)

        craftTable = itemFlipTable(self.launcher)
        layout.addWidget(craftTable)

    def subscribeToEvents(self):
        self.eventSubscribe("ITEMLIST_ITEM_CHANGED", self.applyItemSelection)
        self.eventSubscribe("CLIENT_ITEMS_LAODED", self.displayItems)

    def displayItems(self):
        # self.setItems(self.launcher.client.items[["NameKey", "Name", "Icon"]])
        items = self.launcher.client.items
        self.itemListTable.setData(items, cols=["Name"], base=True)

    def setItems(self, items, filtered=False):
        if not filtered:
            self.model._baseData = items

        self.model._data = items["Name"]
        self.model._icons = items["Icon"]
        index0 = self.model.createIndex(0, 0)
        index1 = self.model.createIndex(len(items), 0)
        self.model.dataChanged.emit(index0, index1)
        self.model.layoutChanged.emit()

    # apply filters
    def onChanged(self, text):

        try:
            re.compile(text)
        except re.error:
            return

        filtered_items = self.model._baseData[
            self.model._baseData["NameKey"].str.contains(text.lower())
        ]
        self.setItems(filtered_items, filtered=True)

    def itemSelectionChanged(self, itemSelection):
        selectedItem = self.tableView.selectionModel().selectedRows()[0]
        row = selectedItem.row()
        cell = self.model.index(row, 0)
        name = cell.data()

        self.eventPush("ITEMLIST_ITEM_CHANGED", name.lower())

    def applyItemSelection(self, name):
        print("applying item selection", name)
        item = self.launcher.client.getItem(name=name)
        if item is None:
            self.eventPush("ITEMLIST_ITEM_DOESNT_EXIST", name)
            return

        self.eventPush("ITEMLIST_ITEM_SELECTED", item)
