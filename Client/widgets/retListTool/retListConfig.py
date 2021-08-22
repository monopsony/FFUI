from .retListConfigBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass


class retListConfig(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.showButton.clicked.connect(self.showRetListTool)
        self.hideButton.clicked.connect(self.hideRetListTool)

    def showRetListTool(self):
        rlTool = self.launcher.uiElements["retListTool"]
        if not rlTool.isHidden():
            return
        rlTool.show()

    def hideRetListTool(self):
        rlTool = self.launcher.uiElements["retListTool"]
        if rlTool.isHidden():
            return

        rlToo.hide()
