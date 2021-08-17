from .columnConfigBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass
from pandas.api.types import is_numeric_dtype

decimalsSettings = {
    0: "{:.0f}",
    1: "{:.1f}",
    2: "{:.2f}",
    3: "{:.3f}",
    4: "{:.4f}",
    5: "{}",
}
decimalSettingsReversed = {v: k for k, v in decimalsSettings.items()}


class columnConfig(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent, pandaTable, colName):
        self.launcher = pandaTable.launcher
        super().__init__(parent)

        self.setupUi(self)
        self.pandaTable = pandaTable

        # apply column
        self.columnName = colName
        self.columnNameLabel.setText(colName)

        # hide decimal thing if column not numeric
        self.numeric = True  # is_numeric_dtype(pandaTable.model._data[colName])
        # TODO is_numeric_dtype is not working properly for some reason idk
        if not self.numeric:
            self.decimalDD.hide()
            self.useKCB.hide()
        else:
            self.decimalDD.show()
            self.useKCB.show()

        self.setConfig()

    def setConfig(self):
        d = self.pandaTable.getConfig(["columns", self.columnName])
        if d is None:
            return
        decimalIndex = decimalSettingsReversed[d.get("decimalFormatting", "{}")]

        self.columnShownCB.setChecked(d.get("shown", True))
        self.decimalDD.setCurrentIndex(decimalIndex)
        self.useKCB.setChecked(d.get("useK", False))

    def getConfig(self):
        decimalSetting = decimalsSettings[self.decimalDD.currentIndex()]
        d = {
            "shown": self.columnShownCB.isChecked(),
            "decimalFormatting": decimalSetting,
            "useK": self.useKCB.isChecked(),
        }
        return d
