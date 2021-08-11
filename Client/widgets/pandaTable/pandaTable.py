from .pandaTableBase import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from Events import EventWidgetClass
import re
import pandas as pd
import logging, traceback

logger = logging.getLogger(__name__)


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

    def data(self, index, role):
        row, col = index.row(), index.column()
        if role == Qt.DisplayRole:
            if self.isSeries:
                a = self.columns[row]
                return str(self._data[a])
            else:
                value = self._data[self.columns[col]].iloc[row]
                return str(value)
            # return "yo"

        if (
            (role == Qt.DecorationRole)
            and (col == self.iconApplicationCol)
            and (self.iconDataCol is not None)
        ):
            value = self._data[self.iconDataCol][row]
            iconId = self.launcher.client.getIconPath(value)
            return QtGui.QIcon(iconId)

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
        self.parent.setData(self._data, sort=col, sortOrder=order)


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
        **kwargs,
    ):
        self.launcher = launcher
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # parameters
        self.eventName = eventName

        # setup model
        model = TableModel(self.launcher, self)
        self.tableView.setModel(model)
        self.model = model
        model.iconApplicationCol = iconApplicationCol
        model.iconDataCol = iconDataCol
        model.parentPandaTable = self

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

        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.tableView.horizontalHeader().setVisible(horizontalHeader)
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

    eventName = None
    filterKey = None

    # apply filters
    def applyFilter(self, text):
        if text is None:
            text = self.filterEdit.text()
            logger.debug(
                f"No text was given to pandatable {type(self)}, found `{text}` instead"
            )

        if (self.filterKey is None) or len(self.model._baseData) == 0:
            return

        try:
            re.compile(text)
        except re.error:
            return

        colData = self.model._baseData[self.filterKey]
        truth = colData.str.contains(text.lower())
        filteredData = self.model._baseData[truth]
        filteredData.reset_index(drop=True, inplace=True)
        self.setData(filteredData)

    lastSortedCol = None
    lastSortOrder = None

    def setData(self, data, cols=None, base=False, sort=None, sortOrder=True):
        self.model.empty = False

        if sort is None:
            sort = self.lastSortedCol
            sortOrder = self.lastSortOrder
        else:
            self.lastSortedCol = sort
            self.lastSortOrder = sortOrder

        if sort is not None:
            try:
                data = data.sort_values(sort, ascending=not sortOrder)
            except Exception as e:
                logger.error(f"Failed to sort by {sort}: {e}")
                logger.error(f"{traceback.format_exc()}")

        isSeries = type(data) == pd.Series
        if cols is None:
            if len(self.model.columns) == 0:
                if isSeries:
                    cols = list(data.index)
                else:
                    cols = data.columns
            else:
                cols = self.model.columns

        self.model.indexNames = data.index

        self.model.isSeries = isSeries
        self.model.columns = cols

        self.model._data = data
        index0 = self.model.createIndex(0, 0)
        index1 = self.model.createIndex(len(data), (isSeries and 1) or len(cols))
        self.model.dataChanged.emit(index0, index1)
        self.model.layoutChanged.emit()

        if base:
            self.model._baseData = data

    def itemSelectionChanged(self):

        if self.eventName is None:
            return

        sel = self.tableView.selectedIndexes()[0]
        row = self.model._data.iloc[sel.row()]
        self.eventPush(self.eventName + "_DATA_SELECTED", row, sel.column())

    def setEmpty(self):
        self.model.empty = True
        self.model.layoutChanged.emit()
