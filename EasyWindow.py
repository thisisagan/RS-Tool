# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EasyWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EasyWindow(object):
    def setupUi(self, EasyWindow):
        EasyWindow.setObjectName("EasyWindow")
        EasyWindow.resize(400, 180)
        EasyWindow.setMinimumSize(QtCore.QSize(400, 180))
        EasyWindow.setMaximumSize(QtCore.QSize(400, 180))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Pictures/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EasyWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(EasyWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(40, 70, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.loadButton.setFont(font)
        self.loadButton.setObjectName("loadButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(210, 70, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 30, 306, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.renishaw_button = QtWidgets.QRadioButton(self.layoutWidget)
        self.renishaw_button.setObjectName("renishaw_button")
        self.select_BG = QtWidgets.QButtonGroup(EasyWindow)
        self.select_BG.setObjectName("select_BG")
        self.select_BG.addButton(self.renishaw_button)
        self.horizontalLayout.addWidget(self.renishaw_button)
        self.ez_button = QtWidgets.QRadioButton(self.layoutWidget)
        self.ez_button.setObjectName("ez_button")
        self.select_BG.addButton(self.ez_button)
        self.horizontalLayout.addWidget(self.ez_button)
        self.iraman_button = QtWidgets.QRadioButton(self.layoutWidget)
        self.iraman_button.setObjectName("iraman_button")
        self.select_BG.addButton(self.iraman_button)
        self.horizontalLayout.addWidget(self.iraman_button)
        EasyWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(EasyWindow)
        self.statusbar.setObjectName("statusbar")
        EasyWindow.setStatusBar(self.statusbar)

        self.retranslateUi(EasyWindow)
        QtCore.QMetaObject.connectSlotsByName(EasyWindow)

    def retranslateUi(self, EasyWindow):
        _translate = QtCore.QCoreApplication.translate
        EasyWindow.setWindowTitle(_translate("EasyWindow", "简单模式"))
        self.loadButton.setText(_translate("EasyWindow", "加载文件"))
        self.saveButton.setText(_translate("EasyWindow", "保存文件"))
        self.renishaw_button.setText(_translate("EasyWindow", "Renishaw"))
        self.ez_button.setText(_translate("EasyWindow", "Ez Raman"))
        self.iraman_button.setText(_translate("EasyWindow", "i Raman Plus"))
