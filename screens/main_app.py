from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui_style import NEON_BACKGROUND

class MainApp(QWidget):
    def __init__(self, username):
        super().__init__()

        self.setWindowTitle("Rubik Solver")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(NEON_BACKGROUND)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        t = QLabel(f"Welcome, {username}")
        t.setFont(QFont("Arial", 32, QFont.Bold))

        layout.addWidget(t)
        self.setLayout(layout)
