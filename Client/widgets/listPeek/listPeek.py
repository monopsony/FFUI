from .listPeekBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox
from Events import EventWidgetClass
import logging

logger = logging.getLogger(__name__)


class listPeek(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.applyList)

        # connect buttons
        self.deleteButton.clicked.connect(self.deleteSelectedList)
        self.editButton.clicked.connect(self.editSelectedList)

    selectedList = None

    def applyList(self, lst, col):
        self.selectedList = lst
        if self.selectedList is None:
            self.label.setText("")
            self.infoLabel.setText("")
            return

        self.titleLabel.setText(lst["Name"])
        client = self.launcher.client

        self.infoLabel.setText(f'Number of items: {len(lst["ItemIds"])}')

    def deleteSelectedList(self):
        if self.selectedList is None:
            return
        lst = self.selectedList
        logger.debug(f'Asking to delete selected list: {self.selectedList["Name"]}')
        reply = QMessageBox.question(
            self,
            f"Delete list",
            f"Are you sure you want to delete list {lst['Name']} of {len(lst['ItemIds'])} items?",
            QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.launcher.client.deleteList(self.selectedList)

    def editSelectedList(self):
        if self.selectedList is None:
            return
        logger.debug(f'Editing selected list: {self.selectedList["Name"]}')

        listCreate = self.launcher.uiElements["listCreate"]
        listCreate.setCurrentList(
            self.selectedList["ItemIds"], name=self.selectedList["Name"]
        )
        self.eventPush("LISTCREATE_LIST_CHANGED")
        self.launcher.uiElements["leftTabs"].tabWidget.setCurrentIndex(2)
