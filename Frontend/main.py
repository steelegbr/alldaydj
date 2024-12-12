from PySide6.QtWidgets import QApplication
from ui.views.launcher import Launcher
from sys import argv

app = QApplication(argv)

window = Launcher()
window.show()

app.exec()
