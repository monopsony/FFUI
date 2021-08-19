from .pandaTableBase import Ui_Form
from .configWindow import configWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass
from collections import defaultdict
from numbers import Number
import re
import pandas as pd
import logging, traceback, copy
from pandas.api.types import is_numeric_dtype

logger = logging.getLogger(__name__)

BASE_PANDATABLE_CONFIG = {
    "columnWidths": {
        "Name": 300,
    }
}

# https://forum.qt.io/topic/96989/how-to-remove-decoration-tinting-of-selected-items-in-item-views/9
# to remove blue tint on icon when selected
def uniformIcon(path):
    icon = QIcon()
    pixmap = QPixmap(path)
    for state in [QIcon.Off, QIcon.On]:
        for mode in [QIcon.Normal, QIcon.Disabled, QIcon.Active, QIcon.Selected]:
            icon.addPixmap(pixmap, mode, state)

    return icon


# QIcon uniformIcon(const QString& path){
#     const QPixmap basePixmap(path);
#     QIcon result;
#     for (auto state : {QIcon::Off, QIcon::On}){
#         for (auto mode : {QIcon::Normal, QIcon::Disabled, QIcon::Active, QIcon::Selected})
#             result.addPixmap(basePixmap, mode, state);
#     }
#     return result;
# }


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, launcher, parent):
        super(TableModel, self).__init__()
        data = pd.DataFrame([])
        self._data = pd.DataFrame([])
        self._baseData = data
        self.launcher = launcher
        self.parent = parent

    iconApplicationCol = -1
    iconDataCol = None
    columns = []
    indexNames = []
    isSeries = False
    empty = True
    formatting = defaultdict(lambda: "{}")
    useK = defaultdict(lambda: False)

    def data(self, index, role):
        row, col = index.row(), index.column()
        if role == Qt.DisplayRole:
            if self.isSeries:
                colName = self.columns[row]
                value = self._data[colName]
                if isinstance(value, Number):
                    form = self.formatting[colName]
                    if self.useK[colName] and (value > 10000):
                        value /= 1000
                        form += "k"
                else:
                    form = "{}"
                return form.format(value)
            else:
                colName = self.columns[col]
                value = self._data[colName].iloc[row]
                if isinstance(value, Number):
                    form = self.formatting[colName]
                    if self.useK[colName] and (value > 10000):
                        value /= 1000
                        form += "k"
                else:
                    form = "{}"
                return form.format(value)
            # return "yo"

        if (
            (role == Qt.DecorationRole)
            and (col == self.iconApplicationCol)
            and (self.iconDataCol is not None)
        ):
            value = self._data[self.iconDataCol].iloc[row]
            iconId = self.launcher.client.getIconPath(value)
            return uniformIcon(iconId)

    def rowCount(self, index):
        if self.empty:
            return 0
        return (self.isSeries and len(self.columns)) or self._data.shape[0]

    def columnCount(self, index):
        if self.empty:
            return 0
        return (self.isSeries and 1) or len(self.columns)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return (self.isSeries and "") or self.columns[section]

            if orientation == Qt.Vertical:
                return (self.isSeries and self.columns[section]) or self.indexNames[
                    section
                ]

    def sort(self, Ncol, order):
        if len(self.columns) == 0:
            return

        col = self.columns[Ncol]
        self.parent.setConfig("sort", (col, order))
        self.parent.refresh()


class pandaTable(EventWidgetClass, QtWidgets.QWidget, Ui_Form):
    def __init__(
        self,
        launcher,
        *args,
        singleRow=False,
        filterKey=None,
        eventName=None,
        verticalHeader=False,
        horizontalHeader=False,
        cellHeight=None,
        cellWidth=None,
        iconApplicationCol=-1,
        iconDataCol=None,
        multiSelect=False,
        sortingEnabled=True,
        configKey="generic",
        hasConfig=True,
        isMenu=False,
        hasQuery=False,
        **kwargs,
    ):
        self.launcher = launcher
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # parameters
        self.eventName = eventName
        self.configKey = configKey

        if isMenu:
            self.widget.setObjectName("menuFrame")
            self.frame.setObjectName("menuFrame")

        self.hasQuery = hasQuery
        if not hasQuery:
            self.queryWidget.hide()
        else:
            self.queryEdit.returnPressed.connect(self.applyQuery)

        # setup model
        model = TableModel(self.launcher, self)
        self.tableView.setModel(model)
        self.model = model
        model.iconApplicationCol = iconApplicationCol
        model.iconDataCol = iconDataCol
        model.parentPandaTable = self

        self.multiSelect = multiSelect
        if not multiSelect:
            # SET SINGLE SELECTION ONLY
            self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.tableView.selectionModel().selectionChanged.connect(
            self.itemSelectionChanged
        )
        self.tableView.setSortingEnabled(sortingEnabled)

        # STYLING
        self.tableView.verticalHeader().setVisible(verticalHeader)
        if cellHeight is not None:
            self.tableView.verticalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Fixed
            )
            self.tableView.verticalHeader().setMinimumSectionSize(cellHeight)
            self.tableView.verticalHeader().setDefaultSectionSize(cellHeight)

        if cellWidth is not None:
            self.tableView.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Fixed
            )
            self.tableView.horizontalHeader().setMinimumSectionSize(cellWidth)
            self.tableView.horizontalHeader().setDefaultSectionSize(cellWidth)

        self.tableView.horizontalHeader().setVisible(horizontalHeader)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.tableView.setIconSize(QSize(40, 40))

        # MAKE READ ONLY
        self.tableView.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # connect filter
        if type(filterKey) == str:
            self.filterEdit.textChanged.connect(self.applyFilter)
            self.filterKey = filterKey
        else:
            self.verticalLayout.removeWidget(self.filterEdit)
            self.filterEdit.deleteLater()
            self.filterEdit.widgetName = False

        # setup config
        if not hasConfig:
            self.configButton.hide()

        # connect other events
        self.tableView.horizontalHeader().sectionResized.connect(self.onColumnResize)
        self.configButton.clicked.connect(self.openConfig)

        # apply configs
        self.applyConfig()

    eventName = None
    filterKey = None

    def filterData(self, data):

        if len(data) == 0:
            return data

        ## SEARCH FILTER
        text = self.getConfig("currentSearch")
        if (self.filterKey is not None) and (len(data) != 0):

            if text is None:
                text = self.filterEdit.text()
                logger.debug(
                    f"No text was given to pandatable {type(self)}, found `{text}` instead"
                )
            try:
                re.compile(text)
                colData = data[self.filterKey]
                truth = colData.str.contains(text.lower())
                data = data[truth]
                data.reset_index(drop=True, inplace=True)
            except re.error:
                pass
            except Exception as e:
                logger.error(f"Exception while applying search filter: {e}")
                logger.error(f"{traceback.format_exc()}")

        ## SEARCH FILTER
        text = self.getConfig("currentQuery")
        if (text is not None) and (text.strip() != "") and (len(data) != 0):

            try:
                data = data.query(text)
                data.reset_index(drop=True, inplace=True)
            except Exception as e:
                logger.error(f"failed to apply current query/filter: {e}")
                logger.error(f"{traceback.format_exc()}")

        return data

    # apply filters
    def applyFilter(self, text):
        self.setConfig("currentSearch", text)
        self.refresh()

    def applyQuery(self):
        text = self.queryEdit.text()
        self.setConfig("currentQuery", text)
        self.refresh()

    def setData(self, data, cols=None, base=False, sort=None, sortOrder=True):
        self.model.empty = False

        if sort is None:
            sortTuple = self.getConfig("sort")
            if sortTuple is not None:
                sort, sortOrder = sortTuple

        if sort is not None:
            try:
                data = data.sort_values(sort, ascending=not sortOrder)
            except Exception as e:
                logger.error(f"Failed to sort by {sort}: {e}")
                logger.error(f"{traceback.format_exc()}")

        isSeries = type(data) == pd.Series
        if cols is None:
            if self.baseColumns is None:
                if isSeries:
                    cols = [x for x in list(data.index) if not "Unnamed" in x]
                else:
                    cols = data.columns
            else:
                cols = self.baseColumns

        self.model.indexNames = data.index

        self.model.isSeries = isSeries
        self.model.columns = cols

        if base:
            self.baseColumns = cols
            self.applyConfig()

        # apply filters
        dataFiltered = self.filterData(data)

        self.model._data = dataFiltered
        index0 = self.model.createIndex(0, 0)
        index1 = self.model.createIndex(
            len(dataFiltered), (isSeries and 1) or len(self.model.columns)
        )
        self.model.dataChanged.emit(index0, index1)
        self.model.layoutChanged.emit()

        if base:
            self.model._baseData = data
            self.applyConfigColumnWidths()
            self.applySortArrow()

    def itemSelectionChanged(self):

        if self.eventName is None:
            return

        if self.multiSelect:
            return

        sel = self.tableView.selectedIndexes()
        if len(sel) == 0:
            self.eventPush(self.eventName + "_DATA_SELECTED", None, None)
        else:
            sel = sel[0]
            row = self.model._data.iloc[sel.row()]
            self.eventPush(self.eventName + "_DATA_SELECTED", row, sel.column())

    empty = False

    def setEmpty(self):
        self.model.empty = True
        self.model.layoutChanged.emit()

    # this method should be replaced for specific implementations of the panda table
    def baseConfigPath(self):
        if self.configKey == "generic":
            logger.critical(
                f"Generic table config used, please use a configKey kwarg or replace the baseConfigPath method. Culprit is: {type(self)}"
            )
            raise ValueError("Generic table config used")
        return ["tables", self.configKey]

    def setConfig(self, path, value):
        if type(path) != list:
            path = [path]

        return self.launcher.setConfig(self.baseConfigPath() + path, value)

    def getConfig(self, path):
        basePath = self.baseConfigPath()
        if self.launcher.getConfig(basePath) is None:
            self.launcher.setConfig(basePath, copy.deepcopy(BASE_PANDATABLE_CONFIG))

        if type(path) != list:
            path = [path]

        return self.launcher.getConfig(self.baseConfigPath() + path)

    def applyConfigColumnWidths(self):
        conf = self.getConfig("columnWidths")
        if conf is None:
            return

        for i in range(len(self.model.columns)):
            colName = self.model.columns[i]
            if colName in conf:
                self.tableView.setColumnWidth(i, conf[colName])

    def applySortArrow(self):
        # set sort arrow correctly
        sortTuple = self.getConfig("sort")
        if sortTuple is None:
            return

        sort, sortOrder = sortTuple

        cols = self.model.columns
        if sort not in cols:
            return

        colIndex = cols.index(sort)

        tv = self.tableView
        tv.horizontalHeader().setSortIndicator(
            colIndex, sortOrder and Qt.DescendingOrder or Qt.AscendingOrder
        )

    baseColumns = None

    def refresh(self):
        if self.empty:
            return
        self.setData(self.model._baseData, base=True)

    def applyConfig(self):
        # self.applyConfigColumnWidths()
        # is done by setData at the end

        if self.baseColumns is None:
            return

        # hide columns
        notShownColumns = []
        for col in self.baseColumns:
            isShown = self.getConfig(["columns", col, "shown"])
            if (isShown is not None) and (isShown == False):
                notShownColumns.append(col)

        self.model.columns = [x for x in self.model.columns if x not in notShownColumns]

        for col in self.model.columns:
            form = "{}"
            form = self.getConfig(["columns", col, "decimalFormatting"])
            if form is not None:
                self.model.formatting[col] = form

            self.model.useK[col] = self.getConfig(["columns", col, "useK"])

        # set search and query to last thing
        # search
        searchText = self.getConfig("currentSearch")
        if self.filterKey is not None:
            self.filterEdit.setText(searchText)

        queryText = self.getConfig("currentQuery")
        if self.hasQuery:
            self.queryEdit.setText(queryText)

    def onColumnResize(self, colIndex, oldSize, newSize):
        col = self.model.columns[colIndex]
        self.setConfig(["columnWidths", col], newSize)

    def openConfig(self):
        if "pandaConfigWindow" not in self.launcher.uiElements:
            self.launcher.uiElements["pandaConfigWindow"] = configWindow(self.launcher)
            logger.debug("pandaConfigWindow created for the first time")

        cw = self.launcher.uiElements["pandaConfigWindow"]
        cw.applySettings(self)
