from abc import ABC, abstractmethod
from enum import StrEnum
from services.logging import LoggingService, Logger


class AudioFileState(StrEnum):
    LOCAL = "Local File"
    REMOTE = "Remote File"
    CACHED = "Cached File"


class AudioFile(ABC):
    state: AudioFileState

    def __init__(self, state: AudioFileState):
        self.state = state

    @abstractmethod
    def get_local_file_path(self):
        pass


class LocalAudioFile(AudioFile):
    __file_path: str

    def __init__(self, file_path: str):
        super().__init__(AudioFileState.LOCAL)
        self.__file_path = file_path

    def get_local_file_path(self):
        return self.__file_path


class RemoteAudioFile(AudioFile):
    __local_file_path: str
    __reference: str

    def __init__(self, reference: str):
        super().__init__(AudioFileState.REMOTE)
        self.__reference = reference

    def get_local_file_path(self):
        return self.__local_file_path


class AudioFileService:
    __logger: Logger

    def __init__(self, logger: Logger = LoggingService().get_logger(__name__)):
        self.__logger = logger

    def get_local_file(self, file_path: str) -> LocalAudioFile:
        self.__logger.info("Supplying a local audio file", file_path=file_path)
        return LocalAudioFile(file_path)

    def get_remote_file(self, reference: str) -> RemoteAudioFile:
        self.__logger.info("Supplying a remote audio file", reference=reference)
        return RemoteAudioFile(reference)
