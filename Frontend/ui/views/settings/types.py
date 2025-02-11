from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from ui.viewmodels.type import CartTypeListModel


class CartTypeSettings(QWidget):
    __add_button: QPushButton
    __add_text: QLineEdit
    __cart_type_list: QListView
    __cart_type_model: CartTypeListModel
    __delete_button: QPushButton

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addLayout(self.__generate_cart_type_list())
        layout.addLayout(self.__generate_delete())
        layout.addLayout(self.__generate_add())

        self.setLayout(layout)

    def __generate_cart_type_list(self):
        layout = QHBoxLayout()

        self.__cart_type_model = CartTypeListModel()

        self.__cart_type_list = QListView()
        self.__cart_type_list.setModel(self.__cart_type_model)
        layout.addWidget(self.__cart_type_list)

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
        cart_type_text = self.__add_text.text()
        if not cart_type_text:
            return

        self.__cart_type_model.addCartType(cart_type_text)
        self.__add_text.clear()

    def __delete_button_pressed(self):
        indexes = self.__cart_type_list.selectedIndexes()
        for index in indexes:
            self.__cart_type_model.deleteCartType(index.row())
