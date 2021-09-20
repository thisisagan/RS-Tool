# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(395, 212)
        self.user_name = QtWidgets.QLineEdit(LoginWindow)
        self.user_name.setGeometry(QtCore.QRect(120, 70, 113, 25))
        self.user_name.setObjectName("user_name")
        self.password = QtWidgets.QLineEdit(LoginWindow)
        self.password.setGeometry(QtCore.QRect(120, 110, 113, 25))
        self.password.setObjectName("password")
        self.login_button = QtWidgets.QPushButton(LoginWindow)
        self.login_button.setGeometry(QtCore.QRect(260, 70, 81, 61))
        self.login_button.setObjectName("login_button")
        self.label = QtWidgets.QLabel(LoginWindow)
        self.label.setGeometry(QtCore.QRect(50, 70, 67, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(LoginWindow)
        self.label_2.setGeometry(QtCore.QRect(50, 110, 67, 21))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "登录"))
        self.login_button.setText(_translate("LoginWindow", "登录"))
        self.label.setText(_translate("LoginWindow", "<html><head/><body><p align=\"center\">用户名</p></body></html>"))
        self.label_2.setText(_translate("LoginWindow", "<html><head/><body><p align=\"center\">密码</p></body></html>"))
