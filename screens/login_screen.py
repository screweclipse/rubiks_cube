from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from screens.home_screen import HomeScreen
from ui_style import NEON_BACKGROUND
from db import get_user_password
from security import verify_password
from screens.signup_screen import SignUpScreen
from screens.main_app import MainApp


class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rubik Solver - Login")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(NEON_BACKGROUND)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Rubik Solver Login")
        title.setFont(QFont("Arial", 34, QFont.Bold))

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)

        signup_btn = QPushButton("Create Account")
        signup_btn.clicked.connect(self.open_signup)

        layout.addWidget(title)
        layout.addWidget(self.user)
        layout.addWidget(self.pwd)
        layout.addWidget(login_btn)
        layout.addWidget(signup_btn)

        self.setLayout(layout)

    def login(self):
        username = self.user.text().strip()
        password = self.pwd.text()

        stored = get_user_password(username)

        if not stored:
            QMessageBox.critical(self, "Error", "User not found")
            return

        if verify_password(password, stored):
            QMessageBox.information(self, "Success", "Logged in!")
            self.main = MainApp(username)
            self.main.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Wrong password")
        self.main = HomeScreen()
        self.main.show()
        self.close()

    def open_signup(self):
        self.signup = SignUpScreen(self)
        self.signup.show()
        self.hide()
