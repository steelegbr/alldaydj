from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from ui.views.settings.tag import TagSettings


class Settings(QWidget):
    def __init__(self):
        super().__init__()

        tabs = QTabWidget(movable=True)
        tabs.addTab(TagSettings(), "Tags")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)
