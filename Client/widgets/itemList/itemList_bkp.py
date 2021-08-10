from .itemListBase import Ui_Form
from widgets.itemPeek.itemPeek import itemPeek
from widgets.itemInfoTable.itemInfoTable import itemInfoTable
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
import os, re
import pandas as pd
from Events import EventWidgetClass


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, launcher, data):
        super(TableModel, self).__init__()
        self.launcher = launcher
        self._data = data

    _icons = pd.DataFrame([1])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # print(index.row(), index.column())
            value = self._data.iloc[index.row()]
            return str(value)

        if role == Qt.DecorationRole:
            value = self._icons.iloc[index.row()]
            iconId = self.launcher.client.getIconPath(value)
            return QtGui.QIcon(iconId)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return 1

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class itemList(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)
        self.subscribeToEvents()
        self.setupUi(self)

        self.lineEdit.textChanged.connect(self.onChanged)

        data = pd.DataFrame(
            [[""]],
            columns=["A"],
        )
        model = TableModel(self.launcher, data)
        # model.setHorizontalHeaderLabels(["N/A"])

        self.tableView.setModel(model)
        # SET SINGLE SELECTION ONLY
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.selectionModel().selectionChanged.connect(
            self.itemSelectionChanged
        )

        self.model = model

        # make it read only
        self.tableView.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # styling
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.tableView.horizontalHeader().setVisible(False)

        self.tableView.setIconSize(QSize(40, 40))

        #### OTHER ELEMENTS
        ## REPLACE PLACEHOLDER ITEM PEEK
        # https://stackoverflow.com/questions/4625102/how-to-replace-a-widget-with-another-using-qt
        peek = itemPeek(self.launcher)
        self.verticalLayout_2.replaceWidget(self.itemPeekPlaceholder, peek)
        self.itemPeek = peek

        ## REPLACE PLACEHOLDER ITEM INFO TABLE
        infoTable = itemInfoTable(self.launcher)
        self.verticalLayout_3.replaceWidget(self.itemInfoTablePlaceholder, infoTable)
        self.itemInfoTable = infoTable

    model = None

    def subscribeToEvents(self):
        self.eventSubscribe("ITEMLIST_ITEM_CHANGED", self.applyItemSelection)
        self.eventSubscribe("CLIENT_ITEMS_LAODED", self.displayItems)

    def displayItems(self):
        print("DISPLAY ITEMS")
        self.setItems(self.launcher.client.items[["NameKey", "Name", "Icon"]])

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
