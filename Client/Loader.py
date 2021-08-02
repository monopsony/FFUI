from PyQt5.QtCore import QObject, QThread, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import time, os
import pandas as pd
from Events import EventClass


class Loader(QObject, EventClass):
    def __init__(self, ui, *args, **kwargs):

        self.ui = ui
        super().__init__(*args, **kwargs)

    def run(self):

        while True:
            time.sleep(0.1)
            self.eventHandle()
