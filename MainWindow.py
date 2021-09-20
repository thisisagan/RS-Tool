# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(246, 155)
        MainWindow.setMinimumSize(QtCore.QSize(246, 155))
        MainWindow.setMaximumSize(QtCore.QSize(246, 155))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Pictures/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.easyButton = QtWidgets.QPushButton(self.centralwidget)
        self.easyButton.setGeometry(QtCore.QRect(60, 30, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.easyButton.setFont(font)
        self.easyButton.setObjectName("easyButton")
        self.proButton = QtWidgets.QPushButton(self.centralwidget)
        self.proButton.setGeometry(QtCore.QRect(60, 80, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.proButton.setFont(font)
        self.proButton.setObjectName("proButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "模式选择"))
        self.easyButton.setText(_translate("MainWindow", "简单模式"))
        self.proButton.setText(_translate("MainWindow", "专业模式"))
