from PyQt5.QtCore import QObject, QThread, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import time, os
import pandas as pd
from Events import EventClass

RECIPES_FILE = "Recipe.csv"
ITEMS_FILE = "Item.csv"
LISTS_DIR = "Lists"


class Client(QObject, EventClass):
    def __init__(self, ui, *args, **kwargs):

        self.ui = ui
        super().__init__(*args, **kwargs)
        self.eventFree = "CLIENT_FREE"  # sends a CLIENT_FREE event whenever the client is done with something that occupied it

    def loadItems(self):
        if not os.path.exists(ITEMS_FILE):
            print(f'No file found under {ITEMS_FILE}. Fetch them using "item update"')
            return

        r = pd.read_csv(ITEMS_FILE)

        # change all Names to titlecase for consistency
        r["Name"] = r["Name"].astype(str).str.title()

        self.items = r
        print(f"Loaded a total of {len(self.items)} items")
        self.eventPush("CLIENT_ITEMS_LAODED")

    def run(self):

        print("starting run")
        self.loadItems()

        while True:
            time.sleep(0.1)
            self.eventHandle()
        print("stopping run")
