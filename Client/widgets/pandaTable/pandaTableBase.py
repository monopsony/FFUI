# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pandaTableBase.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 666)
        Form.setMinimumSize(QtCore.QSize(270, 0))
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.configButton = QtWidgets.QToolButton(self.frame)
        self.configButton.setObjectName("configButton")
        self.horizontalLayout.addWidget(self.configButton)
        self.filterEdit = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterEdit.sizePolicy().hasHeightForWidth())
        self.filterEdit.setSizePolicy(sizePolicy)
        self.filterEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.filterEdit.setObjectName("filterEdit")
        self.horizontalLayout.addWidget(self.filterEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setMinimumSectionSize(30)
        self.tableView.verticalHeader().setCascadingSectionResizes(False)
        self.tableView.verticalHeader().setDefaultSectionSize(45)
        self.tableView.verticalHeader().setMinimumSectionSize(42)
        self.verticalLayout.addWidget(self.tableView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.configButton.setText(_translate("Form", "S"))
