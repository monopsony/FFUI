from .quickPreviewBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from widgets.pandaTable.pandaTable import pandaTable
import pandas as pd
from widgets.itemPeek.itemPeek import itemPeek
from Events import EventWidgetClass
from widgets.other.tables import qpItemCraftTable, qpItemFlipTable
import logging

logger = logging.getLogger(__name__)


class quickPreviewTool(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
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

        self.eventSubscribe("CLIPBOARD_CHANGED", self.clipboardEvent)
        self.eventSubscribe("CRAFTING_ITEMS", self.conditionalShow)

        # set config
        if self.launcher.getConfig(["quickPreviewTool", "stayOnTop"]):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # add qpItemCraftTable
        self.itemCraftTable = qpItemCraftTable(self.launcher)
        self.verticalLayout.addWidget(self.itemCraftTable)

        # add qpItemFlipTable
        self.itemFlipTable = qpItemFlipTable(self.launcher)
        self.verticalLayout.addWidget(self.itemFlipTable)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)

        for i in range(5):
            self.verticalLayout.setStretch(i, 0)
        self.verticalLayout.setStretch(5, 1)

    currentList = set()

    def conditionalShow(self):
        show = self.launcher.getConfig(["quickPreviewTool", "showAutomatically"])
        if show:
            self.show()
            self.setFocus()

    active = False

    def showEvent(self, arg):
        logger.info("Opening quick preview tool")
        self.active = True
        self.launcher.startClipboardWatcher()

    def hideEvent(self, arg):
        logger.info("Closing quick preview tool")
        self.active = False
        self.launcher.checkClipboardWatch()

    def setClipboardLabel(self, value):
        if value is None:
            self.label.setText("Clipboard: N/A")
        else:
            value = value[:40] + "..." if (len(value) > 40) else value
            self.label.setText(f"Clipboard: {value}")

    def clipboardEvent(self, newValue, oldValue):
        if not self.active:
            return
        self.setClipboardLabel(newValue)
        if newValue is None:
            return
        client = self.launcher.client
        item = client.getItem(name=newValue)

        if item is None:
            self.itemCraftTable.updateSelectedItem(item)
            return

        logger.info(f"Quick preview tool: item found in clipboard: {newValue}")
        self.itemPeek.applyItem(item)

        self.itemCraftTable.updateSelectedItem(item)
        self.itemFlipTable.updateSelectedItem(item)
