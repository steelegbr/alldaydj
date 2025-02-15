from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from ui.views.settings.genres import GenreSettings
from ui.views.settings.sound import SoundSettings
from ui.views.settings.types import CartTypeSettings
from ui.views.settings.tag import TagSettings


class Settings(QWidget):
    def __init__(self):
        super().__init__()

        tabs = QTabWidget(movable=True)
        tabs.addTab(SoundSettings(), "Sound")
        tabs.addTab(CartTypeSettings(), "Cart Types")
        tabs.addTab(GenreSettings(), "Genres")
        tabs.addTab(TagSettings(), "Tags")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)
