from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (
    QObject,
    QThread,
    pyqtSignal,
    QSortFilterProxyModel,
    QTimer,
)
from widgets.itemList.itemList import itemList
from widgets.listCreate.listCreate import listCreate
from widgets.listsList.listsList import listsList
from widgets.leftTabs.leftTabs import leftTabs
from Client.Client import Client
from Loader import Loader
import sys, traceback, os, json
from Events import EventClass
import logging

# import qtmodern.styles
# import qtmodern.windows

logger = logging.getLogger(__name__)


class Launcher(EventClass):
    def __init__(self):
        super().__init__()

    uiElements = {}

    def initUi(self):

        # CREATE LEFT TABS
        ltwidget = leftTabs(self)
        self.uiElements["leftTabs"] = ltwidget

        # CREATE ITEM LIST
        ilwidget = itemList(self)
        self.uiElements["itemList"] = ilwidget

        ltwidget.itemsTab = ilwidget
        ltwidget.tabWidget.addTab(ilwidget, "Items")

        # CREATE LIST LIST
        llwidget = listsList(self)
        self.uiElements["listsList"] = llwidget

        ltwidget.listsListTab = llwidget
        ltwidget.tabWidget.addTab(llwidget, "Lists")

        # CREATE CREATE LIST
        clwidget = listCreate(self)
        self.uiElements["listCreate"] = clwidget

        ltwidget.createListsTab = clwidget
        ltwidget.tabWidget.addTab(clwidget, "Create List")

        self.uiElements["leftTabs"].show()

    def launch(self):

        self.loadConfigFile()

        app = QtWidgets.QApplication(sys.argv)
        style = open("stylesheet_bkp.qss").read()
        app.setStyle("Fusion")
        app.setStyleSheet(style)

        self.app = app
        # print(dir(qtmodern.styles))
        # qtmodern.styles.light(app)
        self.initUi()

        self.clientThread = QThread()
        self.client = Client(self.uiElements, self)
        self.client.moveToThread(self.clientThread)

        self.clientThread.started.connect(self.client.run)
        self.clientThread.start()

        self.loaderThread = QThread()
        self.loader = Loader(self.uiElements)
        self.loader.moveToThread(self.loaderThread)
        self.loader.client = self.client
        self.client.loader = self.loader

        self.loaderThread.started.connect(self.loader.run)
        self.loaderThread.start()

        # SET TIMER FOR EVENT LOOP
        timer = QtCore.QTimer()
        timer.timeout.connect(self.eventHandle)
        timer.setInterval(int(0.1 * 1000))  # milliseconds
        timer.start()

        # SEND INITIALIZATION PROCEDURE FOR THINGS THAT NEED TO BE DONE IN THEIR OWN THREADS
        # FOR EXAMPLE ASYNCIO INITIALIZATION FOR THE CONNECTOR
        self.eventPush("CLIENT_INIT")

        # EXECUTE MAIN LOOP
        app.exec_()

        self.exit()

    def exit(self):
        self.closeThreads()
        self.saveConfigFile()

        # sys.exit(0)

    def loadConfigFile(self):
        with open("config.json", "r") as f:
            p = json.load(f)

        self.config = p

    def saveConfigFile(self):
        with open("config.json", "w") as f:
            f.write(json.dumps(self.config, indent=2, sort_keys=True))

    def getConfig(self, path):
        if type(path) != list:
            return self.config.get(path, None)
        d = self.config
        for x in path:
            d = d.get(x, None)
            if d is None:
                return None

        return d

    def setConfig(self, path, value):
        if type(path) != list:
            path = [path]
        oldValue = self.getConfig(path)
        d = self.config
        for x in path[:-1]:
            if x not in d:
                d[x] = {}
            d = d[x]

        d[path[-1]] = value

    def ping(self):
        logger.info("ping")

    def closeThreads(self):
        logger.info("Terminated threads")
        self.clientThread.terminate()
        self.loaderThread.terminate()

    def waitForEvents(self):
        app.processEvents()  # Qt events
        self.eventHandle()  # custom events


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
    )
    launch = Launcher()
    launch.launch()
