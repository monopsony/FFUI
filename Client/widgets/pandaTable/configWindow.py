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

    isPopupWindow = True

    def applySettings(self, pandaTable):
        baseConfigPath = pandaTable.baseConfigPath()
        self.label.setText(f'Table config: `{".".join(baseConfigPath)}`')

        cols = pandaTable.model.columns
        layout = self.mainLayout

        for x in cols:
            if (x == "Name") or ("Unnamed" in x):
                continue

            layout.addWidget(columnConfig(self, pandaTable, x))

        self.show()
        getattr(self, "raise")()  # cant just self.raise cause raise is a keyword
        self.activateWindow()
