# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'retListConfigBase.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(616, 98)
        Form.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolConfigWidget = QtWidgets.QWidget(Form)
        self.toolConfigWidget.setObjectName("toolConfigWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.toolConfigWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.titleLabel = QtWidgets.QLabel(self.toolConfigWidget)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout_2.addWidget(self.titleLabel)
        self.frame = QtWidgets.QFrame(self.toolConfigWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.showButton = QtWidgets.QPushButton(self.frame)
        self.showButton.setObjectName("showButton")
        self.horizontalLayout.addWidget(self.showButton)
        self.hideButton = QtWidgets.QPushButton(self.frame)
        self.hideButton.setObjectName("hideButton")
        self.horizontalLayout.addWidget(self.hideButton)
        spacerItem = QtWidgets.QSpacerItem(454, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.toolConfigWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.titleLabel.setText(_translate("Form", "Retainer Listings"))
        self.showButton.setText(_translate("Form", "Show"))
        self.hideButton.setText(_translate("Form", "Hide"))
