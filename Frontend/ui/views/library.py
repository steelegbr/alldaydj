from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
)


class Library(QWidget):
    __clear_button: QPushButton
    __new_cart_button: QPushButton
    __search_box: QLineEdit
    __result_count: QLabel
    __search_label: QLabel

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addLayout(self.__generate_search_bar())
        layout.addLayout(self.__generate_results())
        layout.addLayout(self.__generate_footer())
        layout.setStretch(1, 1)

        self.setLayout(layout)

    def __generate_search_bar(self):
        search_layout = QHBoxLayout()
        self.__search_label = QLabel("Search:")
        search_layout.addWidget(self.__search_label)

        self.__search_box = QLineEdit()
        search_layout.addWidget(self.__search_box)

        self.__clear_button = QPushButton("Clear")
        search_layout.addWidget(self.__clear_button)

        search_layout.setStretch(1, 1)

        return search_layout

    def __generate_results(self):
        results_layout = QHBoxLayout()

        results_layout.addWidget(QLabel("Results"))

        return results_layout

    def __generate_footer(self):
        footer_layout = QHBoxLayout()

        self.__result_count = QLabel("XXX cart(s) found")
        footer_layout.addWidget(self.__result_count)

        self.__new_cart_button = QPushButton("Add Cart")
        footer_layout.addWidget(self.__new_cart_button)

        footer_layout.setStretch(0, 1)

        return footer_layout
