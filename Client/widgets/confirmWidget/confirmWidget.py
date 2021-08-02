from .confirmWidgetBase import Ui_confirmWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass


class confirmWidget(EventWidgetClass, QtWidgets.QWidget, Ui_confirmWidget):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.confirmButton.clicked.connect(self.handleClick)

    def setText(self, text):
        self.label.setText(text)

    def handleClick(self, *args):
        self.onClick(*args)

    def onClick(self, *args):
        pass

    def checkVisibility(self):
        return True

    def applyVisibility(self, *args, **kwargs):
        show = self.checkVisibility()

        if show:
            self.show()
        else:
            self.hide()
