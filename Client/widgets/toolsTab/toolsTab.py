from .toolsTabBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass
from widgets.retListTool.retListTool import retListTool
from widgets.retListTool.retListConfig import retListConfig


class toolsTab(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.setupConfigs()
        self.setupTools()

    def setupConfigs(self):
        layout = self.verticalLayout_2

        rlConfig = retListConfig(self.launcher)
        layout.addWidget(rlConfig)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)

    def setupTools(self):

        rlTool = retListTool(self.launcher)
        rlTool.hide()
        self.launcher.uiElements["retListTool"] = rlTool
