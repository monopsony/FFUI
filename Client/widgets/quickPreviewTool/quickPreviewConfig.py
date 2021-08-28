from .quickPreviewConfigBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass
import logging

logger = logging.getLogger(__name__)


class quickPreviewConfig(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.showButton.clicked.connect(self.showQuickPreviewTool)
        self.hideButton.clicked.connect(self.hideQuickPreviewTool)

        auto = launcher.getConfig(["quickPreviewTool", "showAutomatically"])
        if auto is None:
            auto = False
        self.openAutoCB.setChecked(auto)
        self.openAutoCB.stateChanged.connect(self.updateShowAutomatically)

        stayOnTop = launcher.getConfig(["quickPreviewTool", "stayOnTop"])
        if stayOnTop is None:
            stayOnTop = False
        self.stayOnToPCB.setChecked(stayOnTop)
        self.stayOnToPCB.stateChanged.connect(self.updateStayOnTop)

    def updateStayOnTop(self, *args):
        checked = self.stayOnToPCB.isChecked()
        self.launcher.setConfig(["quickPreviewTool", "stayOnTop"], checked)
        w = self.launcher.uiElements["quickPreviewTool"]
        if checked:
            w.setWindowFlags(w.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            w.setWindowFlags(w.windowFlags() & ~Qt.WindowStaysOnTopHint)

        logger.info(f"Setting quick preview tool stay on top to {checked}")

    def updateShowAutomatically(self, *args):
        checked = self.openAutoCB.isChecked()
        self.launcher.setConfig(["quickPreviewTool", "showAutomatically"], checked)
        logger.info(f"Setting quick preview tool automatic showing to {checked}")

    def showQuickPreviewTool(self):
        qpTool = self.launcher.uiElements["quickPreviewTool"]
        if not qpTool.isHidden():
            return
        qpTool.show()

    def hideQuickPreviewTool(self):
        qpTool = self.launcher.uiElements["quickPreviewTool"]
        if qpTool.isHidden():
            return

        qpTool.hide()
