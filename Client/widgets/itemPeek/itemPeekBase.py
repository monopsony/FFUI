# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itemPeekBase.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(918, 107)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.topFrame = QtWidgets.QFrame(Form)
        self.topFrame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.topFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topFrame.setObjectName("topFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.topFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.itemImage = QtWidgets.QLabel(self.topFrame)
        self.itemImage.setMinimumSize(QtCore.QSize(50, 50))
        self.itemImage.setMaximumSize(QtCore.QSize(50, 50))
        self.itemImage.setText("")
        self.itemImage.setPixmap(QtGui.QPixmap("../../000000.png"))
        self.itemImage.setScaledContents(False)
        self.itemImage.setObjectName("itemImage")
        self.horizontalLayout.addWidget(self.itemImage)
        self.titleLabel = QtWidgets.QLabel(self.topFrame)
        self.titleLabel.setStyleSheet("")
        self.titleLabel.setObjectName("titleLabel")
        self.horizontalLayout.addWidget(self.titleLabel)
        self.verticalLayout.addWidget(self.topFrame)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.titleLabel.setText(_translate("Form", "N/A"))
        self.label_2.setText(_translate("Form", "itemType"))
