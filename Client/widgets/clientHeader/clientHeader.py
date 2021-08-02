from .clientHeaderBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass


class clientHeader(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.eventSubscribe("CLIENT_FREE", self.setFree)
        self.eventSubscribe("CLIENT_BUSY", self.setBusy)
        self.eventSubscribe("CLIENT_PROGRESS", self.setBusy)

    def setFree(self):
        self.label.setText("Client is free")
        self.label.setStyleSheet("color: #648b46;")
        self.progressBar.hide()

    def setBusy(self, *args):
        client = self.launcher.client
        if not client.busy:
            return self.setFree()

        if client.progressText is None:
            self.label.setText("Client is busy")
        else:
            self.label.setText(client.progressText)
        self.label.setStyleSheet("color: #984343;")

        if client.currentMax > 1:
            self.progressBar.show()
            self.progressBar.setMaximum(client.currentMax)
            self.progressBar.setValue(client.currentProgress)
        else:
            self.progressBar.hide()

    def refresh(self):
        client = self.launcher.client
        if client.busy:
            self.setBusy()
        else:
            self.setFree()
