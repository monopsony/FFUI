# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listCraftToolsBase.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 41)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 9, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.craftSelectedButton = QtWidgets.QPushButton(Form)
        self.craftSelectedButton.setObjectName("craftSelectedButton")
        self.horizontalLayout.addWidget(self.craftSelectedButton)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.craftTopButton = QtWidgets.QPushButton(Form)
        self.craftTopButton.setObjectName("craftTopButton")
        self.horizontalLayout.addWidget(self.craftTopButton)
        self.craftTopEdit = QtWidgets.QLineEdit(Form)
        self.craftTopEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.craftTopEdit.setDragEnabled(False)
        self.craftTopEdit.setClearButtonEnabled(False)
        self.craftTopEdit.setObjectName("craftTopEdit")
        self.horizontalLayout.addWidget(self.craftTopEdit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout.setStretch(4, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.craftSelectedButton.setText(_translate("Form", "Craft Selected"))
        self.craftTopButton.setText(_translate("Form", "Craft Top:"))
