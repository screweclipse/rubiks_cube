from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from password_checklist import PasswordChecklist
from ui_style import NEON_BACKGROUND
from security import is_strong_password, hash_password
from db import add_user


class SignUpScreen(QWidget):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window
        self.setWindowTitle("Create Account")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(NEON_BACKGROUND)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # ---- Title ----
        title = QLabel("Create Account")
        title.setFont(QFont("Arial", 30))
        layout.addWidget(title)

        # ---- Username ----
        self.user = QLineEdit()
        self.user.setPlaceholderText("Choose Username")
        layout.addWidget(self.user)

        # ---- Password Row (Password + Eye Button) ----
        pwd_row = QHBoxLayout()
        pwd_row.setAlignment(Qt.AlignCenter)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Choose Password")
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setFixedWidth(350)

        self.eye_btn = QPushButton("👁")
        self.eye_btn.setFixedWidth(50)
        self.eye_btn.setStyleSheet("font-size: 20px; background: transparent; color: #7ec8ff; border: none;")
        self.eye_btn.clicked.connect(self.toggle_password_visibility)

        pwd_row.addWidget(self.pwd)
        pwd_row.addWidget(self.eye_btn)

        layout.addLayout(pwd_row)

        # ---- Password Checklist ----
        self.checklist = PasswordChecklist()
        layout.addWidget(self.checklist)

        self.pwd.textChanged.connect(self.check_password_live)

        # ---- Create Account Button ----
        create_btn = QPushButton("Create Account")
        create_btn.clicked.connect(self.create_account)
        layout.addWidget(create_btn)

        self.setLayout(layout)

        self.password_visible = False


    # ----------------- Show / Hide Password -----------------

    def toggle_password_visibility(self):
        if self.password_visible:
            self.pwd.setEchoMode(QLineEdit.Password)
            self.eye_btn.setText("👁")
            self.password_visible = False
        else:
            self.pwd.setEchoMode(QLineEdit.Normal)
            self.eye_btn.setText("🙈")
            self.password_visible = True


    # ----------------- Live password check -----------------

    def check_password_live(self):
        password = self.pwd.text()
        self.checklist.update_password(password)


    # ----------------- Create account -----------------

    def create_account(self):
        username = self.user.text().strip()
        password = self.pwd.text()

        if username == "":
            QMessageBox.critical(self, "Error", "Username cannot be empty")
            return

        if not is_strong_password(password):
            QMessageBox.critical(
                self, "Weak Password",
                "Password must be:\n"
                "- 8+ chars\n"
                "- Uppercase\n"
                "- Lowercase\n"
                "- Number\n"
                "- Special character (!@#$...)"
            )
            return

        hashed = hash_password(password)

        if not add_user(username, hashed):
            QMessageBox.critical(self, "Error", "User already exists")
            return

        QMessageBox.information(self, "Success", "Account created successfully!")
        self.close()
        self.login_window.show()
