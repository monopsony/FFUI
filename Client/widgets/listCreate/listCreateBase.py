# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listCreateBase.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1289, 893)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.leftLayout = QtWidgets.QVBoxLayout(self.frame)
        self.leftLayout.setObjectName("leftLayout")
        self.itemListTablePlaceholder = QtWidgets.QWidget(self.frame)
        self.itemListTablePlaceholder.setObjectName("itemListTablePlaceholder")
        self.leftLayout.addWidget(self.itemListTablePlaceholder)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addSelectionButton = QtWidgets.QPushButton(self.frame_4)
        self.addSelectionButton.setObjectName("addSelectionButton")
        self.horizontalLayout_2.addWidget(self.addSelectionButton)
        self.addAllButton = QtWidgets.QPushButton(self.frame_4)
        self.addAllButton.setObjectName("addAllButton")
        self.horizontalLayout_2.addWidget(self.addAllButton)
        self.verticalLayout.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.applyFiltersButton = QtWidgets.QPushButton(self.frame_5)
        self.applyFiltersButton.setObjectName("applyFiltersButton")
        self.horizontalLayout_3.addWidget(self.applyFiltersButton)
        self.clearFiltersButton = QtWidgets.QPushButton(self.frame_5)
        self.clearFiltersButton.setObjectName("clearFiltersButton")
        self.horizontalLayout_3.addWidget(self.clearFiltersButton)
        self.verticalLayout.addWidget(self.frame_5)
        self.itemFilterBox = QtWidgets.QGroupBox(self.frame_2)
        self.itemFilterBox.setObjectName("itemFilterBox")
        self.formLayout = QtWidgets.QFormLayout(self.itemFilterBox)
        self.formLayout.setObjectName("formLayout")
        self.canHqLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.canHqLabel.setObjectName("canHqLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.canHqLabel)
        self.canHqDD = QtWidgets.QComboBox(self.itemFilterBox)
        self.canHqDD.setObjectName("canHqDD")
        self.canHqDD.addItem("")
        self.canHqDD.addItem("")
        self.canHqDD.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.canHqDD)
        self.minItemLevelLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.minItemLevelLabel.setObjectName("minItemLevelLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.minItemLevelLabel)
        self.minItemLevelEdit = QtWidgets.QLineEdit(self.itemFilterBox)
        self.minItemLevelEdit.setObjectName("minItemLevelEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.minItemLevelEdit)
        self.maxItemLevelLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.maxItemLevelLabel.setObjectName("maxItemLevelLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.maxItemLevelLabel)
        self.maxItemLevelEdit = QtWidgets.QLineEdit(self.itemFilterBox)
        self.maxItemLevelEdit.setObjectName("maxItemLevelEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.maxItemLevelEdit)
        self.glamourousLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.glamourousLabel.setObjectName("glamourousLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.glamourousLabel)
        self.glamourousDD = QtWidgets.QComboBox(self.itemFilterBox)
        self.glamourousDD.setObjectName("glamourousDD")
        self.glamourousDD.addItem("")
        self.glamourousDD.addItem("")
        self.glamourousDD.addItem("")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.glamourousDD)
        self.minStackSizeLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.minStackSizeLabel.setObjectName("minStackSizeLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.minStackSizeLabel)
        self.minStackSizeEdit = QtWidgets.QLineEdit(self.itemFilterBox)
        self.minStackSizeEdit.setObjectName("minStackSizeEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.minStackSizeEdit)
        self.craftableLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.craftableLabel.setObjectName("craftableLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.craftableLabel)
        self.craftableDD = QtWidgets.QComboBox(self.itemFilterBox)
        self.craftableDD.setObjectName("craftableDD")
        self.craftableDD.addItem("")
        self.craftableDD.addItem("")
        self.craftableDD.addItem("")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.craftableDD)
        self.minEquipLevelLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.minEquipLevelLabel.setObjectName("minEquipLevelLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.minEquipLevelLabel)
        self.maxEquipLevelLabel = QtWidgets.QLabel(self.itemFilterBox)
        self.maxEquipLevelLabel.setObjectName("maxEquipLevelLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.maxEquipLevelLabel)
        self.minEquipLevelEdit = QtWidgets.QLineEdit(self.itemFilterBox)
        self.minEquipLevelEdit.setObjectName("minEquipLevelEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.minEquipLevelEdit)
        self.maxEquipLevelEdit = QtWidgets.QLineEdit(self.itemFilterBox)
        self.maxEquipLevelEdit.setObjectName("maxEquipLevelEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.maxEquipLevelEdit)
        self.verticalLayout.addWidget(self.itemFilterBox)
        self.recipeFIlterBox = QtWidgets.QGroupBox(self.frame_2)
        self.recipeFIlterBox.setObjectName("recipeFIlterBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.recipeFIlterBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.carpenterLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.carpenterLabel.setObjectName("carpenterLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.carpenterLabel)
        self.carpenterCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.carpenterCB.setText("")
        self.carpenterCB.setChecked(True)
        self.carpenterCB.setObjectName("carpenterCB")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.carpenterCB)
        self.blacksmithLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.blacksmithLabel.setObjectName("blacksmithLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.blacksmithLabel)
        self.blacksmithCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.blacksmithCB.setText("")
        self.blacksmithCB.setChecked(True)
        self.blacksmithCB.setObjectName("blacksmithCB")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.blacksmithCB)
        self.armorerLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.armorerLabel.setObjectName("armorerLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.armorerLabel)
        self.armorerCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.armorerCB.setText("")
        self.armorerCB.setChecked(True)
        self.armorerCB.setObjectName("armorerCB")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.armorerCB)
        self.goldsmithLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.goldsmithLabel.setObjectName("goldsmithLabel")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.goldsmithLabel)
        self.goldsmithCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.goldsmithCB.setText("")
        self.goldsmithCB.setChecked(True)
        self.goldsmithCB.setObjectName("goldsmithCB")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.goldsmithCB)
        self.leatherworkerLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.leatherworkerLabel.setObjectName("leatherworkerLabel")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.leatherworkerLabel)
        self.leatherworkerCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.leatherworkerCB.setText("")
        self.leatherworkerCB.setChecked(True)
        self.leatherworkerCB.setObjectName("leatherworkerCB")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.leatherworkerCB)
        self.weaverLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.weaverLabel.setObjectName("weaverLabel")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.weaverLabel)
        self.weaverCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.weaverCB.setText("")
        self.weaverCB.setChecked(True)
        self.weaverCB.setObjectName("weaverCB")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.weaverCB)
        self.alchemistLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.alchemistLabel.setObjectName("alchemistLabel")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.alchemistLabel)
        self.alchemistCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.alchemistCB.setText("")
        self.alchemistCB.setChecked(True)
        self.alchemistCB.setObjectName("alchemistCB")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.alchemistCB)
        self.culinarianLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.culinarianLabel.setObjectName("culinarianLabel")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.culinarianLabel)
        self.culinarianCB = QtWidgets.QCheckBox(self.recipeFIlterBox)
        self.culinarianCB.setText("")
        self.culinarianCB.setChecked(True)
        self.culinarianCB.setObjectName("culinarianCB")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.culinarianCB)
        self.minMasteryLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.minMasteryLabel.setObjectName("minMasteryLabel")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.minMasteryLabel)
        self.minMasteryDD = QtWidgets.QComboBox(self.recipeFIlterBox)
        self.minMasteryDD.setObjectName("minMasteryDD")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.minMasteryDD.addItem("")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.minMasteryDD)
        self.maxMasteryLabel = QtWidgets.QLabel(self.recipeFIlterBox)
        self.maxMasteryLabel.setObjectName("maxMasteryLabel")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.maxMasteryLabel)
        self.maxMasteryDD = QtWidgets.QComboBox(self.recipeFIlterBox)
        self.maxMasteryDD.setObjectName("maxMasteryDD")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.maxMasteryDD.addItem("")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.maxMasteryDD)
        self.verticalLayout.addWidget(self.recipeFIlterBox)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout.setStretch(4, 1)
        self.horizontalLayout.addWidget(self.frame_2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.rightFrame = QtWidgets.QFrame(Form)
        self.rightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rightFrame.setObjectName("rightFrame")
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightFrame)
        self.rightLayout.setObjectName("rightLayout")
        self.frame_6 = QtWidgets.QFrame(self.rightFrame)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.saveButton = QtWidgets.QPushButton(self.frame_6)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_4.addWidget(self.saveButton)
        self.saveNameLabel = QtWidgets.QLabel(self.frame_6)
        self.saveNameLabel.setObjectName("saveNameLabel")
        self.horizontalLayout_4.addWidget(self.saveNameLabel)
        self.saveNameEdit = QtWidgets.QLineEdit(self.frame_6)
        self.saveNameEdit.setObjectName("saveNameEdit")
        self.horizontalLayout_4.addWidget(self.saveNameEdit)
        self.rightLayout.addWidget(self.frame_6)
        self.label = QtWidgets.QLabel(self.rightFrame)
        self.label.setObjectName("label")
        self.rightLayout.addWidget(self.label)
        self.clearFrame = QtWidgets.QFrame(self.rightFrame)
        self.clearFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.clearFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.clearFrame.setObjectName("clearFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.clearFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.removeSelectionButton = QtWidgets.QPushButton(self.clearFrame)
        self.removeSelectionButton.setObjectName("removeSelectionButton")
        self.horizontalLayout_5.addWidget(self.removeSelectionButton)
        self.clearButton = QtWidgets.QPushButton(self.clearFrame)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout_5.addWidget(self.clearButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.rightLayout.addWidget(self.clearFrame)
        self.listItemListPlaceholder = QtWidgets.QWidget(self.rightFrame)
        self.listItemListPlaceholder.setObjectName("listItemListPlaceholder")
        self.rightLayout.addWidget(self.listItemListPlaceholder)
        self.rightLayout.setStretch(3, 1)
        self.horizontalLayout.addWidget(self.rightFrame)
        self.horizontalLayout.setStretch(3, 1)

        self.retranslateUi(Form)
        self.maxMasteryDD.setCurrentIndex(8)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addSelectionButton.setText(_translate("Form", "Add Selection"))
        self.addAllButton.setText(_translate("Form", "Add All"))
        self.applyFiltersButton.setText(_translate("Form", "Apply Filters"))
        self.clearFiltersButton.setText(_translate("Form", "Clear Filters"))
        self.itemFilterBox.setTitle(_translate("Form", "Item filters"))
        self.canHqLabel.setText(_translate("Form", "Can Hq"))
        self.canHqDD.setItemText(0, _translate("Form", "Either"))
        self.canHqDD.setItemText(1, _translate("Form", "Can Hq"))
        self.canHqDD.setItemText(2, _translate("Form", "Cannot Hq"))
        self.minItemLevelLabel.setText(_translate("Form", "Min Item Level"))
        self.maxItemLevelLabel.setText(_translate("Form", "Max Item Level"))
        self.glamourousLabel.setText(_translate("Form", "Glamourous"))
        self.glamourousDD.setItemText(0, _translate("Form", "Either"))
        self.glamourousDD.setItemText(1, _translate("Form", "Glamourous"))
        self.glamourousDD.setItemText(2, _translate("Form", "Not Glamourous"))
        self.minStackSizeLabel.setText(_translate("Form", "Min Stack Size"))
        self.craftableLabel.setText(_translate("Form", "Craftable"))
        self.craftableDD.setItemText(0, _translate("Form", "Either"))
        self.craftableDD.setItemText(1, _translate("Form", "Craftable"))
        self.craftableDD.setItemText(2, _translate("Form", "Not Craftable"))
        self.minEquipLevelLabel.setText(_translate("Form", "Min Equip Level"))
        self.maxEquipLevelLabel.setText(_translate("Form", "Max Equip Level"))
        self.recipeFIlterBox.setTitle(_translate("Form", "Recipe filters"))
        self.carpenterLabel.setText(_translate("Form", "Carpenter"))
        self.blacksmithLabel.setText(_translate("Form", "Blacksmith"))
        self.armorerLabel.setText(_translate("Form", "Armorer"))
        self.goldsmithLabel.setText(_translate("Form", "Goldsmith"))
        self.leatherworkerLabel.setText(_translate("Form", "Leatherworker"))
        self.weaverLabel.setText(_translate("Form", "Weaver"))
        self.alchemistLabel.setText(_translate("Form", "Alchemist"))
        self.culinarianLabel.setText(_translate("Form", "Culinarian"))
        self.minMasteryLabel.setText(_translate("Form", "Min Mastery Recipe"))
        self.minMasteryDD.setItemText(0, _translate("Form", "0"))
        self.minMasteryDD.setItemText(1, _translate("Form", "1"))
        self.minMasteryDD.setItemText(2, _translate("Form", "2"))
        self.minMasteryDD.setItemText(3, _translate("Form", "3"))
        self.minMasteryDD.setItemText(4, _translate("Form", "4"))
        self.minMasteryDD.setItemText(5, _translate("Form", "5"))
        self.minMasteryDD.setItemText(6, _translate("Form", "6"))
        self.minMasteryDD.setItemText(7, _translate("Form", "7"))
        self.minMasteryDD.setItemText(8, _translate("Form", "8"))
        self.maxMasteryLabel.setText(_translate("Form", "Max Mastery Recipe"))
        self.maxMasteryDD.setItemText(0, _translate("Form", "0"))
        self.maxMasteryDD.setItemText(1, _translate("Form", "1"))
        self.maxMasteryDD.setItemText(2, _translate("Form", "2"))
        self.maxMasteryDD.setItemText(3, _translate("Form", "3"))
        self.maxMasteryDD.setItemText(4, _translate("Form", "4"))
        self.maxMasteryDD.setItemText(5, _translate("Form", "5"))
        self.maxMasteryDD.setItemText(6, _translate("Form", "6"))
        self.maxMasteryDD.setItemText(7, _translate("Form", "7"))
        self.maxMasteryDD.setItemText(8, _translate("Form", "8"))
        self.saveButton.setText(_translate("Form", "Save"))
        self.saveNameLabel.setText(_translate("Form", "Name:"))
        self.label.setText(_translate("Form", "Total number of items: /"))
        self.removeSelectionButton.setText(_translate("Form", "Remove selection"))
        self.clearButton.setText(_translate("Form", "Clear"))
