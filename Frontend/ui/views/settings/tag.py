from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from ui.viewmodels.tag import TagListModel


class TagSettings(QWidget):
    __add_button: QPushButton
    __add_text: QLineEdit
    __tag_list: QListView
    __tag_model: TagListModel

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addLayout(self.__generate_tag_list())
        layout.addLayout(self.__generate_delete())
        layout.addLayout(self.__generate_add())

        self.setLayout(layout)

    def __generate_tag_list(self):
        layout = QHBoxLayout()

        self.__tag_model = TagListModel()

        self.__tag_list = QListView()
        self.__tag_list.setModel(self.__tag_model)
        layout.addWidget(self.__tag_list)

        return layout

    def __generate_delete(self):
        layout = QHBoxLayout()

        layout.addWidget(QLabel(""), 1)
        layout.addWidget(QPushButton("Delete"))

        return layout

    def __generate_add(self):
        layout = QHBoxLayout()

        self.__add_text = QLineEdit()
        layout.addWidget(self.__add_text, 1)

        self.__add_button = QPushButton("Add")
        layout.addWidget(self.__add_button)

        return layout
