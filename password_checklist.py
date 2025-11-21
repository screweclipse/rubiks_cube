from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import re


class PasswordChecklist(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("Password Strength Requirements:")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setStyleSheet("color: #7ec8ff; margin-bottom: 10px;")

        self.layout.addWidget(self.title)

        # Individual criteria
        self.criteria = {
            "length": QLabel("✘ At least 8 characters"),
            "upper": QLabel("✘ Contains uppercase letter (A–Z)"),
            "lower": QLabel("✘ Contains lowercase letter (a–z)"),
            "digit": QLabel("✘ Contains a digit (0–9)"),
            "special": QLabel("✘ Contains special character (!@#$%^&*)")
        }

        for label in self.criteria.values():
            label.setFont(QFont("Arial", 13))
            label.setStyleSheet("color: #ff6961;")  # red
            self.layout.addWidget(label)

    def update_password(self, password):
        # Length
        if len(password) >= 8:
            self._set_ok("length")
        else:
            self._set_fail("length")

        # Uppercase
        if re.search(r"[A-Z]", password):
            self._set_ok("upper")
        else:
            self._set_fail("upper")

        # Lowercase
        if re.search(r"[a-z]", password):
            self._set_ok("lower")
        else:
            self._set_fail("lower")

        # Digit
        if re.search(r"[0-9]", password):
            self._set_ok("digit")
        else:
            self._set_fail("digit")

        # Special
        if re.search(r"[!@#$%^&*()_+\-=\\|[\]{};:'\",.<>/?]", password):
            self._set_ok("special")
        else:
            self._set_fail("special")

    def _set_ok(self, key):
        self.criteria[key].setText("✔ " + self.criteria[key].text()[2:])
        self.criteria[key].setStyleSheet("color: #7CFC00;")  # neon green

    def _set_fail(self, key):
        self.criteria[key].setText("✘ " + self.criteria[key].text()[2:])
        self.criteria[key].setStyleSheet("color: #ff6961;")  # neon red
