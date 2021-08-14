from .columnConfigBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass
from pandas.api.types import is_numeric_dtype


class columnConfig(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent, pandaTable, colName):
        self.launcher = pandaTable.launcher
        super().__init__(parent)

        self.setupUi(self)

        # apply column
        self.columnNameLabel.setText(colName)

        # hide decimal thing if column not numeric
        self.numeric = is_numeric_dtype(pandaTable.model._data[colName])
        if not self.numeric:
            self.decimalDD.hide()
            self.useKCB.hide()
        else:
            self.decimalDD.show()
            self.useKCB.show()
