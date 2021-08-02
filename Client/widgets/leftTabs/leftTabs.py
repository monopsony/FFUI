from .leftTabsBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from widgets.clientHeader.clientHeader import clientHeader


class leftTabs(QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        header = clientHeader(self.launcher)
        self.verticalLayout.replaceWidget(self.clientHeaderPlaceholder, header)
        self.clientHeader = header
        self.clientHeaderPlaceholder.hide()  # idk why this one needed hiding but not the others
