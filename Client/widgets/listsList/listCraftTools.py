from .listCraftToolsBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass


class listCraftTools(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, table, *args, **kwargs):
        self.launcher = launcher
        self.table = table
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.craftTopEdit.setValidator(QtGui.QIntValidator(0, 99))

        self.craftSelectedButton.clicked.connect(self.craftSelected)
        self.craftTopButton.clicked.connect(self.craftTop)

    def craftSelected(self):
        tbl = self.table
        items = tbl.getSelectedItems()

        self.launcher.client.ffxivCraftItems(items)

    def craftTop(self):
        tbl = self.table
        N = self.craftTopEdit.text()
        try:
            N = int(N)
        except TypeError:
            return
        except ValueError:
            return

        items = tbl.getTopItems(N)
        self.launcher.client.ffxivCraftItems(items)
