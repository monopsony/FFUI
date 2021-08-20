from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMenuBar, QMainWindow, QMessageBox
from PyQt5.QtCore import (
    QObject,
    QThread,
    pyqtSignal,
    QSortFilterProxyModel,
    QTimer,
    Qt,
)
from widgets.itemList.itemList import itemList
from widgets.listCreate.listCreate import listCreate
from widgets.listsList.listsList import listsList
from widgets.leftTabs.leftTabs import leftTabs
from Client.Client import Client
from Loader import Loader
import sys, traceback, os, json
import pandas as pd
from Events import EventClass
import logging

# import qtmodern.styles
# import qtmodern.windows

logger = logging.getLogger(__name__)

BASE_CONFIG = {
    "connectedWorlds": ["Lich", "Odin", "Phoenix", "Zodiark", "Twintania"],
    "currentListings": [],  # list of item ids
    "nSemaphores": 3,
    "retainerBlacklist": [
        # list of retainer names
    ],
    "world": "Shiva",
}


class Launcher(EventClass):
    def __init__(self):
        super().__init__()

        self.eventSubscribe("ASK_LOAD_MBINFO_CACHE", self.mbinfoCachePrompt)

    uiElements = {}

    version = "1.1.1"

    def initUi(self):

        # create main window
        mainWindow = QMainWindow()
        self.uiElements["mainWindow"] = mainWindow
        self.mainWindow = mainWindow
        mainWindow.resize(1700, 1200)
        mainWindow.setWindowTitle("Sapphire Avenue Exchange")
        # self.mainWindow.setWindowFlags(Qt.FramelessWindowHint)

        self.createMenuBar()

        # CREATE LEFT TABS
        ltwidget = leftTabs(self)
        self.uiElements["leftTabs"] = ltwidget
        self.mainWindow.setCentralWidget(ltwidget)

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

        self.mainWindow.show()

    def createMenuBar(self):
        menubar = QMenuBar(self.mainWindow)
        self.mainWindow.setMenuBar(menubar)

    def mbinfoCachePrompt(self, dt):
        reply = QMessageBox.question(
            self.mainWindow,
            f"MBInfo in cache",
            f"Found market board information in the cache, generated {dt//60:.0f} minutes {dt%60:.0f} seconds ago. Do you want to re-load?\n\nWhen NOT to reload from cache:\n- New metrics were added\n- Blacklists/Current listings were changed\n- Prices are likely to be out of date",
            QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No,
        )
        if reply == QMessageBox.No:
            return

        mbInfoPath = os.path.join("Cache", "mbInfoC.csv")
        self.client.mbInfo = pd.read_csv(mbInfoPath, index_col=0)
        logger.info(
            f"Successfully loaded {len(self.client.mbInfo)} MBInfo entries from cache"
        )
        # self.eventPush("CLIENT_MBINFO_UPDATE")

    def launch(self):

        self.loadConfigFile()

        app = QtWidgets.QApplication(sys.argv)
        style = open(os.path.join("stylesheets", "custom.qss")).read()
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

        # self.loaderThread = QThread()
        # self.loader = Loader(self.uiElements)
        # self.loader.moveToThread(self.loaderThread)
        # self.loader.client = self.client
        # self.client.loader = self.loader

        # self.loaderThread.started.connect(self.loader.run)
        # self.loaderThread.start()

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

        if not os.path.exists("config.json"):
            with open("config.json", "w+") as f:
                f.write(json.dumps(BASE_CONFIG, indent=2, sort_keys=True))

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
        # self.loaderThread.terminate()

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
