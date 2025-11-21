from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui_style import NEON_BACKGROUND
from screens.login_screen import LoginScreen

class EnterScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rubik Solver - Welcome")
        self.setFixedSize(1000, 700)

        self.setStyleSheet(NEON_BACKGROUND)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Rubiks Solver")
        title.setFont(QFont("Arial", 50, QFont.Bold))

        enter_btn = QPushButton("ENTER")
        enter_btn.setFixedSize(300, 70)
        enter_btn.setFont(QFont("Arial", 24, QFont.Bold))
        enter_btn.clicked.connect(self.open_login)

        layout.addWidget(title)
        layout.addSpacing(80)
        layout.addWidget(enter_btn)
        self.setLayout(layout)

    def open_login(self):
        self.login = LoginScreen()
        self.login.show()
        self.close()
