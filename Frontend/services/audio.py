from enum import StrEnum
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaDevices, QMediaPlayer
from services.file import AudioFile
from services.logging import Logger, LoggingService
from services.settings import Settings, SettingsService
from typing import List, Optional


class AudioPlayerState(StrEnum):
    IDLE = "Idle"
    LOADING = "Loading"
    ERROR = "Error"
    PAUSED = "Paused"
    PLAYING = "Playing"


class AudioPlayer:
    __audio_file: AudioFile
    __logger: Logger
    __output: QAudioOutput
    __player: QMediaPlayer
    __state: AudioPlayerState

    def __init__(
        self,
        audio_file: AudioFile,
        output: QAudioOutput,
        logger: Logger = LoggingService().get_logger(__name__),
    ):
        self.__audio_file = audio_file
        self.__logger = logger
        self.__output = output
        self.__state = AudioPlayerState.IDLE

        self.__player = QMediaPlayer()
        self.__player.errorOccurred.connect(self.__handle_error)
        self.__player.mediaStatusChanged.connect(self.__handle_state_change)
        self.__player.setAudioOutput(self.__output)
        self.__player.setSource(
            QUrl.fromLocalFile(self.__audio_file.get_local_file_path())
        )

        self.__logger.info(
            "Audio player created",
            audio_file=self.__audio_file.get_local_file_path(),
            output=output,
        )

    def __handle_error(self, error: QMediaPlayer.Error, message: str):
        self.__state = AudioPlayerState.ERROR
        self.__logger.error(
            "Audio player error",
            error=error,
            message=message,
            file=self.__audio_file.get_local_file_path(),
        )

    def __handle_state_change(self, status: QMediaPlayer.MediaStatus):
        self.__logger.info("Audio player state changed", status=status)

    def close(self):
        pass


class AudioService:
    __logger: Logger
    __settings_service: SettingsService

    def __init__(
        self,
        logger: Logger = LoggingService().get_logger(__name__),
        settings_service: SettingsService = SettingsService(),
    ):
        self.__logger = logger

    def get_output_devices(self) -> List[str]:
        return [device.description() for device in QMediaDevices.audioOutputs()]

    def __description_to_device(self, description: str) -> Optional[QAudioOutput]:
        for device in QMediaDevices.audioOutputs():
            if device.description() == description:
                return device

        self.__logger.error(f"Audio device not found", description=description)
        return self.__get_default_device()

    def __get_default_device(self) -> Optional[QAudioOutput]:
        default_device = QMediaDevices.defaultAudioOutput()
        self.__logger.info(
            f"Obtainig default audio device", description=default_device.description()
        )
        return default_device

    def get_preview_player(self, audio_file: AudioFile) -> AudioPlayer:
        preview_device_name = self.__settings_service.get().sound_device_preview
        preview_device = self.__description_to_device(preview_device_name)
        self.__logger.info(
            f"Creating preview player",
            audio_file=audio_file,
            preview_device=preview_device,
        )
        return AudioPlayer(audio_file, preview_device)
