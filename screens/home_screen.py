from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rubik Solver - Home")
        self.setFixedSize(1000, 700)

        # Neon green background
        self.setStyleSheet("""
            QWidget {
                background-color: #001400;
                background-image:
                    radial-gradient(circle at 50% 30%, rgba(0,255,120,0.25), transparent 60%),
                    linear-gradient(135deg, rgba(0,70,20,0.8), rgba(0,30,10,1));
            }

            QLabel {
                color: #7cff9c;
            }

            QPushButton {
                background: #00cc66;
                color: black;
                padding: 15px;
                font-size: 20px;
                border-radius: 20px;
                width: 260px;
            }

            QPushButton:hover {
                background: #00ff88;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Top text
        title = QLabel("so what are we solving?")
        title.setFont(QFont("Arial", 28, QFont.Bold))

        layout.addWidget(title)
        layout.addSpacing(80)  # space instead of "ch"

        # Bottom buttons row
        buttons_row = QHBoxLayout()
        buttons_row.setAlignment(Qt.AlignCenter)

        # Buttons
        btn_camera = QPushButton("camera (scan cube)")
        btn_random = QPushButton("random solve")

        buttons_row.addWidget(btn_camera)
        buttons_row.addSpacing(50)
        buttons_row.addWidget(btn_random)

        layout.addLayout(buttons_row)

        self.setLayout(layout)
