from enum import StrEnum
from PySide6.QtMultimedia import QAudioOutput
from services.file import AudioFile
from services.logging import Logger, LoggingService


class AudioPlayerState(StrEnum):
    IDLE = "Idle"
    LOADING = "Loading"
    ERROR = "Error"
    PAUSED = "Paused"
    PLAYING = "Playing"


class AudioPlayer:
    __audio_file: AudioFile
    __output: QAudioOutput
    __state: AudioPlayerState

    def __init__(self, audio_file: AudioFile, output: QAudioOutput):
        self.__audio_file = audio_file
        self.__output = output
        self.__state = AudioPlayerState.IDLE


class AudioService:
    __logger = Logger

    def __init__(self, logger: Logger = LoggingService().get_logger(__name__)):
        self.__logger = logger
