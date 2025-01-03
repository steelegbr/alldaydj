from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from ui.views.clock import Clock
from ui.views.placeholder import Placeholder


class MainScreen(QMainWindow):
    __clock: Clock

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AllDay DJ")

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.__create_header())
        main_layout.addLayout(self.__create_tabs())

        main_layout.setStretch(1, 1)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def __create_header(self):
        header = QHBoxLayout()

        self.__clock = Clock()

        header.addWidget(self.__clock)
        header.addWidget(Placeholder("Immediate Log"))
        header.addWidget(Placeholder("Main Controls"))

        return header

    def __create_tabs(self):
        tabs_layout = QHBoxLayout()

        tabs_layout.addWidget(self.__create_left_tabs())
        tabs_layout.addWidget(self.__create_right_tabs())

        return tabs_layout

    @staticmethod
    def __create_left_tabs():
        left_tabs = QTabWidget(movable=True)

        left_tabs.addTab(Placeholder("Log"), "Log")
        left_tabs.addTab(Placeholder("Hotkeys"), "Hotkeys")

        return left_tabs

    @staticmethod
    def __create_right_tabs():
        right_tabs = QTabWidget(movable=True)

        right_tabs.addTab(Placeholder("Library"), "Library")
        right_tabs.addTab(Placeholder("Settings"), "Settings")

        return right_tabs
