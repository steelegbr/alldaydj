from models.dto.audio import Cart, CartType, Genre, Tag
from pathlib import Path
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)
from services.audio import AudioPlayer, AudioService
from services.factory import ServiceFactory
from services.file import AudioFile, AudioFileService


class CartEditor(QDialog):
    __album: QLineEdit
    __artist: QLineEdit
    __audio_file: AudioFile
    __audio_player: AudioPlayer
    __audio_service: AudioService
    __cart: Cart
    __file_button: QPushButton
    __file_path: QLabel
    __file_service: AudioFileService
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

    def __init__(
        self,
        cart: Cart = None,
        audio_service: AudioService = ServiceFactory().audioService(),
        file_service: AudioFileService = ServiceFactory().audioFileService(),
    ):
        super().__init__()

        # if not cart:
        #     cart = Cart()

        # self.__cart = cart
        self.__audio_service = audio_service
        self.__file_service = file_service

        layout = QVBoxLayout()
        layout.addLayout(self.__generate_main_form())
        layout.addLayout(self.__generate_footer())

        self.setLayout(layout)
        self.showMaximized()

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

        self.__file_button = QPushButton("Browse")
        self.__file_path = QLabel("")

        self.__file_button.clicked.connect(self.__file_browse)

        form_layout.addRow("File:", self.__file_path)
        form_layout.addRow("", self.__file_button)

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

    def __file_browse(self):
        audio_file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Audio File", str(Path.home()), "Audio Files (*.mp3 *.wav )"
        )

        if audio_file_path:
            self.__audio_file = self.__file_service.get_local_file(audio_file_path)
            self.__file_path.setText(audio_file_path)
            self.__audio_player = self.__audio_service.get_preview_player(
                self.__audio_file
            )
