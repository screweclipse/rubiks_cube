import sys
import json
import socket
import re

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

HOST = "127.0.0.1"
PORT = 5000

# ------------- client socket helper -------------

def send_request(action, payload):
    req = {"action": action}
    req.update(payload)
    data = json.dumps(req).encode("utf-8")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        s.sendall(data)
        resp_bytes = s.recv(4096)
    except OSError:
        return {"status": "error", "message": "Cannot connect to server"}
    finally:
        s.close()
    try:
        return json.loads(resp_bytes.decode("utf-8"))
    except Exception:
        return {"status": "error", "message": "Invalid server response"}

# ------------- password checklist widget -------------

class PasswordChecklist(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Password Strength Requirements:")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #7ec8ff; margin-bottom: 10px;")
        layout.addWidget(title)

        self.criteria = {
            "length": QLabel("✘ At least 8 characters"),
            "upper": QLabel("✘ Contains uppercase letter (A–Z)"),
            "lower": QLabel("✘ Contains lowercase letter (a–z)"),
            "digit": QLabel("✘ Contains a digit (0–9)"),
            "special": QLabel("✘ Contains special character (!@#$%^&*)"),
        }

        for lbl in self.criteria.values():
            lbl.setFont(QFont("Arial", 12))
            lbl.setStyleSheet("color: #ff6961;")
            layout.addWidget(lbl)

    def update_password(self, password: str):
        self._set_state("length", len(password) >= 8)
        self._set_state("upper", bool(re.search(r"[A-Z]", password)))
        self._set_state("lower", bool(re.search(r"[a-z]", password)))
        self._set_state("digit", bool(re.search(r"[0-9]", password)))
        self._set_state("special", bool(re.search(r"[!@#$%^&*()_+\-=\\|[\]{};:'\",.<>/?]", password)))

    def _set_state(self, key, ok: bool):
        lbl = self.criteria[key]
        text = lbl.text()
        base = text[2:] if len(text) > 2 else text
        if ok:
            lbl.setText("✔ " + base)
            lbl.setStyleSheet("color: #7CFC00;")  # green
        else:
            lbl.setText("✘ " + base)
            lbl.setStyleSheet("color: #ff6961;")  # red

# ------------- simple neon style -------------

NEON_BACKGROUND = """
QWidget {
    background-color: #001022;
    background-image:
        radial-gradient(circle at 50% 30%, rgba(0,150,255,0.35), transparent 60%),
        linear-gradient(135deg, rgba(0,40,85,0.8), rgba(0,15,35,1));
}
QLabel {
    color: #cbe6ff;
}
QLineEdit {
    width: 350px;
    padding: 12px;
    border-radius: 8px;
    background: #041a33;
    border: 2px solid #0e5bff;
    color: white;
    font-size: 18px;
}
QLineEdit:focus {
    border: 2px solid #5aa4ff;
}
QPushButton {
    width: 260px;
    padding: 12px;
    background: #0e5bff;
    color: white;
    font-size: 18px;
    border-radius: 10px;
}
QPushButton:hover {
    background: #3385ff;
}
"""

# ------------- main app after login -------------

class MainApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Rubik Solver - Client")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(NEON_BACKGROUND)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        t = QLabel(f"Welcome, {username}")
        t.setFont(QFont("Arial", 32, QFont.Bold))
        t2 = QLabel("Rubik Solver Ready (connected to server)")
        t2.setFont(QFont("Arial", 18))
        layout.addWidget(t)
        layout.addWidget(t2)
        self.setLayout(layout)

# ------------- signup screen -------------

class SignUpScreen(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.password_visible = False

        self.setWindowTitle("Create Account")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(NEON_BACKGROUND)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Create Account")
        title.setFont(QFont("Arial", 30))
        layout.addWidget(title)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Choose Username")
        layout.addWidget(self.user)

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

        self.checklist = PasswordChecklist()
        layout.addWidget(self.checklist)

        self.pwd.textChanged.connect(self.check_password_live)

        create_btn = QPushButton("Create Account")
        create_btn.clicked.connect(self.create_account)
        layout.addWidget(create_btn)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.password_visible:
            self.pwd.setEchoMode(QLineEdit.Password)
            self.eye_btn.setText("👁")
            self.password_visible = False
        else:
            self.pwd.setEchoMode(QLineEdit.Normal)
            self.eye_btn.setText("🙈")
            self.password_visible = True

    def check_password_live(self):
        self.checklist.update_password(self.pwd.text())

    def create_account(self):
        username = self.user.text().strip()
        password = self.pwd.text()
        if not username or not password:
            QMessageBox.critical(self, "Error", "Username and password cannot be empty")
            return

        resp = send_request("signup", {"username": username, "password": password})
        status = resp.get("status")
        msg = resp.get("message", "")
        if status == "ok":
            QMessageBox.information(self, "Success", msg or "Account created")
            self.close()
            self.login_window.show()
        elif status == "weak_password":
            QMessageBox.critical(self, "Weak Password", msg)
        else:
            QMessageBox.critical(self, "Error", msg or "Signup failed")

# ------------- login screen -------------

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rubik Solver - Login (Client)")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(NEON_BACKGROUND)
        self.password_visible = False

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Rubik Solver Login")
        title.setFont(QFont("Arial", 34, QFont.Bold))
        layout.addWidget(title)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")
        layout.addWidget(self.user)

        pwd_row = QHBoxLayout()
        pwd_row.setAlignment(Qt.AlignCenter)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setFixedWidth(350)

        self.eye_btn = QPushButton("👁")
        self.eye_btn.setFixedWidth(50)
        self.eye_btn.setStyleSheet("font-size: 20px; background: transparent; color: #7ec8ff; border: none;")
        self.eye_btn.clicked.connect(self.toggle_password_visibility)

        pwd_row.addWidget(self.pwd)
        pwd_row.addWidget(self.eye_btn)
        layout.addLayout(pwd_row)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)

        signup_btn = QPushButton("Create Account")
        signup_btn.clicked.connect(self.open_signup)

        layout.addWidget(login_btn)
        layout.addWidget(signup_btn)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.password_visible:
            self.pwd.setEchoMode(QLineEdit.Password)
            self.eye_btn.setText("👁")
            self.password_visible = False
        else:
            self.pwd.setEchoMode(QLineEdit.Normal)
            self.eye_btn.setText("🙈")
            self.password_visible = True

    def login(self):
        username = self.user.text().strip()
        password = self.pwd.text()
        if not username or not password:
            QMessageBox.critical(self, "Error", "Username and password cannot be empty")
            return

        resp = send_request("login", {"username": username, "password": password})
        status = resp.get("status")
        msg = resp.get("message", "")
        if status == "ok":
            QMessageBox.information(self, "Success", msg or "Login successful")
            self.main = MainApp(username)
            self.main.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", msg or "Login failed")

    def open_signup(self):
        self.signup = SignUpScreen(self)
        self.signup.show()
        self.hide()

# ------------- enter screen -------------

class EnterScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rubiks Solver - Welcome")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(NEON_BACKGROUND)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Rubiks Solver")
        title.setFont(QFont("Arial", 50, QFont.Bold))
        layout.addWidget(title)

        enter_btn = QPushButton("ENTER")
        enter_btn.setFixedSize(300, 70)
        enter_btn.setFont(QFont("Arial", 24, QFont.Bold))
        enter_btn.clicked.connect(self.open_login)

        layout.addSpacing(80)
        layout.addWidget(enter_btn)

        self.setLayout(layout)

    def open_login(self):
        self.login = Login()
        self.login.show()
        self.close()

# ------------- main -------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnterScreen()
    window.show()
    sys.exit(app.exec_())
