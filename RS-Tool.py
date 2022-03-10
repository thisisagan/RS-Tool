from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from MainWindow import *
from EasyWindow import *
from ProWindow import *
from EasyMode import *
from ProMode import *
from ValidMode import *
from LoginWindow import *
from ValidWindow import *
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
        valid_window = ValidWindow()
        self.easyButton.clicked.connect(lambda: easy_window.show())
        self.proButton.clicked.connect(lambda: pro_window.show())
        self.validButton.clicked.connect(lambda: valid_window.show())


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
        self.peak_location.setValidator(QtGui.QIntValidator())  # 设置只能输入int类型的数据
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


class ValidWindow(QMainWindow, Ui_ValidWindow):
    def __init__(self, parent=None):
        super(ValidWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.peak_location.setValidator(QtGui.QIntValidator())  # 设置只能输入int类型的数据
        self.reporter_browser.setAcceptRichText(True)
        self.my_init()
        self.set_default()

    def my_init(self):
        valid_mod = ValidMode(self)
        self.load_blank_button.clicked.connect(lambda: valid_mod.load_blank())
        self.valid_button.clicked.connect(lambda: valid_mod.valid())

    def set_default(self):
        self.renishaw_select_button.setChecked(True)
        self.method2_button.setChecked(True)


if __name__ == "__main__":
    from sys import argv, exit
    app = QtWidgets.QApplication(argv)
    login_window = LoginWindow()
    login_window.show()
    exit(app.exec_())
