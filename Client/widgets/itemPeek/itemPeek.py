from .itemPeekBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass


class itemPeek(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, suppressEventSubscribe=False, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        if not suppressEventSubscribe:
            self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.applyItem)

    def applyItem(self, item, col=0):
        self.titleLabel.setText(item["Name"])
        client = self.launcher.client

        icon_path = client.getIconPath(item["Icon"])
        if icon_path is not None:
            w, h = self.itemImage.width(), self.itemImage.height()
            self.itemImage.setPixmap(
                QtGui.QPixmap(icon_path).scaled(w, h, Qt.KeepAspectRatio)
            )

        uiCat = item["ItemUICategory"]
        uiCatName = client.csvData["ItemUICategory"].iloc[uiCat]["Name"]
        self.label_2.setText(uiCatName)
