from .retListToolBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from widgets.pandaTable.pandaTable import pandaTable
import pandas as pd
from widgets.itemPeek.itemPeek import itemPeek
from Events import EventWidgetClass
import logging

logger = logging.getLogger(__name__)


class retListTool(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.launcher.clipboardDependencies.append(self)

        # ITEM PEEK
        peek = itemPeek(self.launcher, suppressEventSubscribe=True)
        self.verticalLayout.replaceWidget(self.itemPeekPlaceholder, peek)
        self.itemPeekPlaceholder.hide()
        self.itemPeek = peek

        # CLEAR BUTTON
        self.clearButton.clicked.connect(self.clearList)

        # TABLE
        table = pandaTable(
            launcher,
            cellHeight=25,
            iconApplicationCol=0,
            iconDataCol="Icon",
            configKey="retListToolTable",
            hasConfig=True,
        )
        self.verticalLayout.replaceWidget(self.pandaTablePlaceholder, table)
        self.pandaTablePlaceholder.hide()
        self.table = table

        self.eventSubscribe("CLIPBOARD_CHANGED", self.clipboardEvent)

    currentList = set()

    def showEvent(self, arg):
        logger.info("Opening retainer listings tool")
        self.launcher.startClipboardWatcher()
        self.currentList = set(self.launcher.getConfig("currentListings"))
        self.updateTable()

    def hideEvent(self, arg):
        logger.info("Closing retainer listings tool")
        self.launcher.checkClipboardWatch()

    def setClipboardLabel(self, value):
        if value is None:
            self.label.setText("Clipboard: N/A")
        else:
            value = value[:40] + "..." if (len(value) > 40) else value
            self.label.setText(f"Clipboard: {value}")

    def clipboardEvent(self, newValue, oldValue):
        self.setClipboardLabel(newValue)
        if newValue is None:
            return
        client = self.launcher.client
        item = client.getItem(name=newValue)

        if item is None:
            return

        logger.info(f"Item found in clipboard: {newValue}")
        self.currentList.add(
            int(item["ItemId"])
        )  # gotta convert it to int to be json-serializable (as opposted to np.int)
        self.launcher.setConfig("currentListings", list(self.currentList))
        self.itemPeek.applyItem(item)
        self.updateTable()

    def clearList(self):
        self.currentList = set()
        self.launcher.setConfig("currentListings", [])
        self.updateTable()

    def updateTable(self):
        lst = self.launcher.getConfig("currentListings")
        df = self.launcher.client.items
        df = df[df["ItemId"].isin(lst)]
        df.reset_index(drop=True, inplace=True)
        self.table.setData(df, cols=["Name", "ItemId"], base=True)
