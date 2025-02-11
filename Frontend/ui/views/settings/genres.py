from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from ui.viewmodels.genre import GenreListModel


class GenreSettings(QWidget):
    __add_button: QPushButton
    __add_text: QLineEdit
    __delete_button: QPushButton
    __genre_list: QListView
    __genre_model: GenreListModel

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addLayout(self.__generate_cart_type_list())
        layout.addLayout(self.__generate_delete())
        layout.addLayout(self.__generate_add())

        self.setLayout(layout)

    def __generate_cart_type_list(self):
        layout = QHBoxLayout()

        self.__genre_model = GenreListModel()

        self.__genre_list = QListView()
        self.__genre_list.setModel(self.__genre_model)
        layout.addWidget(self.__genre_list)

        return layout

    def __generate_delete(self):
        layout = QHBoxLayout()

        layout.addWidget(QLabel(""), 1)

        self.__delete_button = QPushButton("Delete")
        self.__delete_button.pressed.connect(self.__delete_button_pressed)
        layout.addWidget(self.__delete_button)

        return layout

    def __generate_add(self):
        layout = QHBoxLayout()

        self.__add_text = QLineEdit()
        self.__add_text.returnPressed.connect(self.__add_button_pressed)
        layout.addWidget(self.__add_text, 1)

        self.__add_button = QPushButton("Add")
        self.__add_button.pressed.connect(self.__add_button_pressed)
        layout.addWidget(self.__add_button)

        return layout

    def __add_button_pressed(self):
        genre_text = self.__add_text.text()
        if not genre_text:
            return

        self.__genre_model.addGenre(genre_text)
        self.__add_text.clear()

    def __delete_button_pressed(self):
        indexes = self.__genre_list.selectedIndexes()
        for index in indexes:
            self.__genre_model.deleteGenre(index.row())
