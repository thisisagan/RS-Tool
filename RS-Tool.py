import os
import numpy as np
import pandas as pd
import os
import sys
from sklearn.ensemble import IsolationForest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from MainWindow import *
from EasyWindow import *
from ProWindow import *
from EasyMode import *
from ProMode import *
from LoadWindow import *
from login import *
from BaselineRemoval import BaselineRemoval


class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.my_init()

    def my_init(self):
        main_window = MainWindow()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(lambda: login(self, main_window))
        self.login_button.clicked.connect(lambda: login(self, main_window))




class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.my_init()

    def my_init(self):
        easy_window = EasyWindow()
        pro_window = ProWindow()
        self.easyButton.clicked.connect(lambda: easy_window.show())
        self.proButton.clicked.connect(lambda: pro_window.show())


class EasyWindow(QMainWindow, Ui_EasyWindow):
    def __init__(self, parent=None):
        super(EasyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.my_init()

    def my_init(self):
        easy_mode = EasyMode(self)
        self.loadButton.clicked.connect(lambda: easy_mode.process())
        self.saveButton.clicked.connect(lambda: easy_mode.save_file())
        self.renishaw_button.setChecked(True)


class ProWindow(QMainWindow, Ui_ProWindow):
    def __init__(self, parent=None):
        super(ProWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.load_label.setAlignment(Qt.AlignCenter)
        self.process_label.setAlignment(Qt.AlignCenter)
        self.save_label.setAlignment(Qt.AlignCenter)
        self.my_init()
        self.set_default()

    def my_init(self):
        pro_mode = ProMode(self)
        self.load_file_button.clicked.connect(lambda: pro_mode.load_file())
        self.load_dir_button.clicked.connect(lambda: pro_mode.load_dir())
        self.process_button.clicked.connect(lambda: pro_mode.process())
        self.save_file_button.clicked.connect(lambda: pro_mode.save_file())

    def set_default(self):
        self.renishaw_select_button.setChecked(True)
        self.no_classify_button.setChecked(True)
        self.single_sv_button.setChecked(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
