import sys
from PyQt5.QtWidgets import QApplication
from db import init_db
from screens.enter_screen import EnterScreen

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = EnterScreen()
    window.show()
    sys.exit(app.exec_())
