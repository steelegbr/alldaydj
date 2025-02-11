from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)


class CartEditor(QDialog):
    __album: QLineEdit
    __artist: QLineEdit
    __genre: QComboBox
    __isrc: QLineEdit
    __label: QLineEdit
    __override_fade: QCheckBox
    __record_label: QLineEdit
    __sweeper: QCheckBox
    __tags: QListView
    __title: QLineEdit
    __type: QComboBox
    __valid_from: QDateTimeEdit
    __valid_until: QDateTimeEdit
    __year: QSpinBox

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addLayout(self.__generate_main_form())
        layout.addLayout(self.__generate_footer())

        self.setLayout(layout)

    def __generate_main_form(self):
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.__label = QLineEdit()
        form_layout.addRow("Label:", self.__label)

        self.__artist = QLineEdit()
        form_layout.addRow("Artist:", self.__artist)

        self.__title = QLineEdit()
        form_layout.addRow("Title:", self.__title)

        self.__album = QLineEdit()
        form_layout.addRow("Album:", self.__album)

        self.__type = QComboBox()
        form_layout.addRow("Type:", self.__type)

        self.__genre = QComboBox()
        form_layout.addRow("Genre:", self.__genre)

        self.__year = QSpinBox()
        self.__year.setMinimum(1800)
        self.__year.setMaximum(9999)
        form_layout.addRow("Year:", self.__year)

        self.__tags = QListView()
        form_layout.addRow("Tags:", self.__tags)

        self.__sweeper = QCheckBox()
        form_layout.addRow("Sweeper:", self.__sweeper)

        self.__override_fade = QCheckBox()
        form_layout.addRow("Override Fade:", self.__override_fade)

        self.__valid_from = QDateTimeEdit()
        form_layout.addRow("Valid From:", self.__valid_from)

        self.__valid_until = QDateTimeEdit()
        form_layout.addRow("Valid Until:", self.__valid_until)

        self.__isrc = QLineEdit()
        form_layout.addRow("ISRC:", self.__isrc)

        self.__record_label = QLineEdit()
        form_layout.addRow("Record Label:", self.__record_label)

        return form_layout

    @staticmethod
    def __generate_footer():
        layout = QHBoxLayout()

        spacer = QLabel()
        layout.addWidget(spacer, 1)

        save_button = QPushButton("Save")
        layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        layout.addWidget(cancel_button)

        return layout
