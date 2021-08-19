from .listCreateBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox
import os, re
import pandas as pd
from Events import EventWidgetClass
from widgets.pandaTable.pandaTable import pandaTable
import logging, datetime, json

logger = logging.getLogger(__name__)


class listCreate(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(self, launcher, *args, **kwargs):
        self.launcher = launcher
        super().__init__(*args, **kwargs)
        self.subscribeToEvents()
        self.setupUi(self)
        self.launcher.uiElements["listCreate"] = self

        ## REPLACE PLACEHOLDER ITEM LIST TABLE
        # https://stackoverflow.com/questions/4625102/how-to-replace-a-widget-with-another-using-qt
        itemListTable = pandaTable(
            launcher,
            filterKey="NameKey",
            eventName="LISTITEMLISTTABLE",
            cellHeight=33,
            iconApplicationCol=0,
            iconDataCol="Icon",
            multiSelect=True,
            configKey="itemListTable",
            hasConfig=True,
            isMenu=True,
        )
        self.leftLayout.replaceWidget(self.itemListTablePlaceholder, itemListTable)
        self.itemListTablePlaceholder.hide()
        self.itemListTable = itemListTable

        ## REPLACE PLACEGOLDER LIST ITEM LIST TABLE
        listItemListTable = pandaTable(
            launcher,
            filterKey="NameKey",
            eventName="LISTITEMLISTTABLE",
            cellHeight=33,
            iconApplicationCol=0,
            iconDataCol="Icon",
            multiSelect=True,
            configKey="listItemListTable",
            hasConfig=False,
        )
        self.rightLayout.replaceWidget(self.listItemListPlaceholder, listItemListTable)
        self.listItemListPlaceholder.hide()
        self.listItemListTable = listItemListTable

        # self.listItemListTable.tableView.setSelectionBehavior(
        #     QtWidgets.QTableView.SelectRows
        # )

        self.connectAllButtons()
        self.applyValidators()

        # inits
        self.craftableFilterChanged()

    model = None

    def connectAllButtons(self):
        self.addAllButton.clicked.connect(self.addAllItems)
        self.addSelectionButton.clicked.connect(self.addSelectedItems)

        self.applyFiltersButton.clicked.connect(self.applyFilters)

        self.saveButton.clicked.connect(self.saveCurrentList)

        self.craftableDD.currentIndexChanged.connect(self.craftableFilterChanged)

        self.clearButton.clicked.connect(self.clearCurrentList)
        self.removeSelectionButton.clicked.connect(self.removeSelection)

    def craftableFilterChanged(self, index=None):
        if index is None:
            index = int(self.craftableDD.currentIndex())

        self.recipeFIlterBox.setEnabled(index == 1)

    def saveCurrentList(self):
        name = self.saveNameEdit.text()
        name = name.strip()
        if name == "":
            msgBox = QMessageBox(
                QMessageBox.Warning, "Empty name", "You need to give the list a name."
            )
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.exec_()
            return

        path = os.path.join("Lists", f"{name}.json")
        if os.path.exists(path):
            reply = QMessageBox.question(
                self,
                f"Duplicate name",
                f"Name `{name}` already exists. Do you want to replace the existing list?",
                QMessageBox.Yes | QMessageBox.No,
                defaultButton=QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return

        d = {
            "LastEdited": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "NumberOfItems": len(self.currentList),
            "ItemIds": list(self.currentList),
        }
        with open(path, "w+") as fil:
            fil.write(json.dumps(d, indent=4))

        self.eventPush("NEW_LIST_SAVED", path)

    def applyValidators(self):
        self.minItemLevelEdit.setValidator(QtGui.QIntValidator(0, 99999))
        self.maxItemLevelEdit.setValidator(QtGui.QIntValidator(0, 99999))
        self.minEquipLevelEdit.setValidator(QtGui.QIntValidator(0, 99999))
        self.maxEquipLevelEdit.setValidator(QtGui.QIntValidator(0, 99999))
        self.minStackSizeEdit.setValidator(QtGui.QIntValidator(0, 999))

    def subscribeToEvents(self):
        self.eventSubscribe("CLIENT_ITEMS_LAODED", self.displayItems)
        self.eventSubscribe("LISTCREATE_LIST_CHANGED", self.applyListChanged)

    def displayItems(self):
        # self.setItems(self.launcher.client.items[["NameKey", "Name", "Icon"]])
        items = self.launcher.client.items
        self.itemListTable.setData(items, cols=["Name"], base=True)

    currentList = set()

    def setCurrentList(self, lst, name=None):
        if type(lst) == dict:
            lst = lst["ItemIds"]
        logger.debug(f"Setting current list to {name} ({len(lst)} items)")

        self.currentList = set(lst)
        if name is not None:
            self.saveNameEdit.setText(name)
        self.eventPush("LISTCREATE_LIST_CHANGED")

    def clearCurrentList(self):
        logger.debug(f"Clearing current list")
        self.currentList = set()
        self.eventPush("LISTCREATE_LIST_CHANGED")

    def removeSelection(self):
        tv = self.listItemListTable.tableView
        selectedIndices = tv.selectionModel().selectedIndexes()
        rows = [x.row() for x in selectedIndices]
        data = self.listItemListTable.model._data

        logger.debug(f"Removing {len(rows)} items from list")

        for row in rows:
            item = int(data.at[data.index[row], "ItemId"])
            self.currentList.remove(item)
        self.eventPush("LISTCREATE_LIST_CHANGED")

    def addSelectedItems(self):
        logging.debug(f"Adding selected items")
        selectedIndices = self.itemListTable.tableView.selectionModel().selectedRows()
        rows = [x.row() for x in selectedIndices]

        data = self.itemListTable.model._data

        for row in rows:
            item = int(data.at[data.index[row], "ItemId"])
            self.currentList.add(item)

        self.eventPush("LISTCREATE_LIST_CHANGED")

    def addAllItems(self):
        logging.debug(f"Adding all items")
        data = self.itemListTable.model._data

        self.currentList.update(list(data["ItemId"]))
        self.eventPush("LISTCREATE_LIST_CHANGED")

    def applyListChanged(self):
        lst = self.currentList
        if self.currentList is None:
            return
        df = self.launcher.client.items
        df = df[df["ItemId"].isin(lst)]
        df.reset_index(drop=True, inplace=True)
        self.listItemListTable.setData(df, cols=["Name", "ItemId"], base=True)
        self.listItemListTable.applyFilter(None)

        self.label.setText(f"Total number of items: {len(df)}")

    # FILTERS
    def getFilters(self):

        ## ITEMS
        itemFilters = []

        # Can Hq
        canHqIdx = self.canHqDD.currentIndex()
        if canHqIdx == 1:
            itemFilters.append("(CanBeHq == True)")
        elif canHqIdx == 2:
            itemFilters.append("(CanBeHq == False)")

        # Min ilvl
        minItemLevel = self.minItemLevelEdit.text()
        if minItemLevel != "":
            itemFilters.append(f"(LevelItem >= {minItemLevel})")

        # Max ilvl
        maxItemLevel = self.maxItemLevelEdit.text()
        if maxItemLevel != "":
            itemFilters.append(f"(LevelItem <= {maxItemLevel})")

        # Min equip
        minEquipLevel = self.minEquipLevelEdit.text()
        if minEquipLevel != "":
            itemFilters.append(f"(LevelEquip >= {minEquipLevel})")

        # Max equip
        maxEquipLevel = self.maxEquipLevelEdit.text()
        if maxEquipLevel != "":
            itemFilters.append(f"(LevelEquip <= {maxEquipLevel})")

        # Min Stack Size
        minStackSize = self.minStackSizeEdit.text()
        if minStackSize != "":
            itemFilters.append(f"(StackSize >= {minStackSize})")

        # Glamourous
        glam = self.glamourousDD.currentIndex()
        if glam == 1:
            itemFilters.append("(Glamourous == True)")
        elif glam == 2:
            itemFilters.append("(Glamourous == False)")

        # Craftable
        craftable = self.craftableDD.currentIndex()
        if craftable == 1:
            itemFilters.append("(Craftable == True)")
        elif craftable == 2:
            itemFilters.append("(Craftable == False)")

        ## RECIPES
        recipeFilters = []

        # JOBS
        jobs = []
        for i, cb in enumerate(
            [
                self.carpenterCB,
                self.blacksmithCB,
                self.armorerCB,
                self.goldsmithCB,
                self.leatherworkerCB,
                self.weaverCB,
                self.alchemistCB,
                self.culinarianCB,
            ]
        ):
            if cb.isChecked():
                jobs.append(i)
        if len(jobs) < 8:
            filters = [f"(CraftType == {i})" for i in jobs]
            recipeFilters.append(f'({" | ".join(filters)})')

        # MASTERY
        minMastery = float(self.minMasteryDD.currentText())
        if minMastery > 0.0:
            recipeFilters.append(f"(MasteryLevel >= {minMastery})")

        maxMastery = float(self.maxMasteryDD.currentText())
        if maxMastery < 8.0:
            recipeFilters.append(f"(MasteryLevel <= {maxMastery})")

        return " & ".join(itemFilters), " & ".join(recipeFilters)

    currentItemFilters = ""
    currentRecipeFilters = ""

    def applyFilters(self):
        iFilters, rFilters = self.getFilters()

        if (iFilters == self.currentItemFilters) and (
            rFilters == self.currentRecipeFilters
        ):
            return

        df = self.launcher.client.items
        if iFilters != "":
            df = df.query(iFilters)

        if (rFilters != "") and "(Craftable == True)" in iFilters:
            df = df.query(rFilters)

        self.currentItemFilters = iFilters
        self.currentRecipeFilters = rFilters
        self.itemListTable.setData(df, cols=["Name"], base=True)
        self.itemListTable.applyFilter(None)
        self.eventPush("LISTITEMLISTTABLE_FILTERS_APPLIED")
