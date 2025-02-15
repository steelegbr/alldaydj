from PySide6.QtWidgets import QComboBox, QFormLayout, QWidget
from services.audio import AudioService
from services.factory import ServiceFactory
from services.settings import Settings, SettingsService
from typing import List


class SoundSettings(QWidget):
    __audio_service: AudioService
    __preview_device: QComboBox
    __settings_service: SettingsService

    def __init__(
        self,
        audio_service: AudioService = ServiceFactory().audioService(),
        settings_service: SettingsService = ServiceFactory().settingsService(),
    ):
        super().__init__()

        self.__audio_service = audio_service
        self.__settings_service = settings_service

        self.setLayout(
            self.__generate_main_layout(
                self.__audio_service.get_output_devices(), self.__settings_service.get()
            )
        )

    def __generate_main_layout(self, sound_cards: List[str], settings: Settings):
        layout = QFormLayout()

        self.__preview_device = QComboBox()
        self.__preview_device.addItems(sound_cards)
        self.__preview_device.setCurrentText(settings.sound_device_preview)
        self.__preview_device.currentTextChanged.connect(
            self.__handle_preview_device_change
        )
        layout.addRow("Preview Device", self.__preview_device)

        return layout

    def __handle_preview_device_change(self, device: str):
        settings = self.__settings_service.get()
        settings.sound_device_preview = device
        self.__settings_service.save(settings)
