from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout


class Placeholder(QWidget):
    __label: QLabel

    def __init__(self, content: str):
        super().__init__()

        self.__label = QLabel(content)

        layout = QVBoxLayout()
        layout.addWidget(self.__label)
        self.setLayout(layout)
