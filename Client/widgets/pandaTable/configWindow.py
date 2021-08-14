from .configWindowBase import Ui_Form
from .columnConfig import columnConfig
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass


class configWindow(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher

        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.applyButton.clicked.connect(self.applyConfig)

    isPopupWindow = True

    pandaTable = None

    colConfigs = []

    def applySettings(self, pandaTable):
        self.pandaTable = pandaTable
        baseConfigPath = pandaTable.baseConfigPath()
        self.label.setText(f'Table config: `{".".join(baseConfigPath)}`')

        if (not hasattr(pandaTable, "baseColumns")) or (pandaTable.baseColumns is None):
            return

        cols = pandaTable.baseColumns
        layout = self.columnsLayout

        # delete old settings
        if len(self.colConfigs) != 0:
            for x in self.colConfigs:
                x.deleteLater()

        self.colConfigs = []
        for x in cols:
            if (x == "Name") or ("Unnamed" in x):
                continue

            colConfig = columnConfig(self, pandaTable, x)
            layout.addWidget(colConfig)
            self.colConfigs.append(colConfig)

        self.show()
        getattr(self, "raise")()  # cant just self.raise cause raise is a keyword
        self.activateWindow()

    def applyConfig(self):
        d = self.getConfig()
        for k in d.keys():
            self.pandaTable.setConfig(k, d[k])

        self.pandaTable.refresh()

    def getConfig(self):
        d = {"columns": {}}
        # general settings

        # columns
        c = d["columns"]
        for colConfig in self.colConfigs:
            col = colConfig.columnName
            c[col] = colConfig.getConfig()

        return d
