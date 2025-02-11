from models.dto.audio import Genre
from PySide6.QtCore import QAbstractListModel, Qt
from services.factory import GenreService, ServiceFactory
from services.logging import Logger, LoggingService
from typing import List


class GenreListModel(QAbstractListModel):
    __genre_service: GenreService
    __genres: List[Genre]
    __logger: Logger

    def __init__(
        self,
        *args,
        genres=None,
        genre_service: GenreService = ServiceFactory().genreService(),
        log_service: LoggingService = LoggingService(),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.__logger = log_service.get_logger(__name__)
        self.__genre_service = genre_service
        self.__genres = genres or []
        self.refresh()

    def refresh(self):
        self.__genre_service.get_all(self.__update_genres, self.__handle_failure)

    def __update_genres(self, genres: List[Genre]):
        self.beginResetModel()
        self.__genres = genres
        self.endResetModel()

    def __handle_failure(self, error: str):
        self.__logger.error(f"Failed reported back to genre viewmodel: {error}")

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.__genres[index.row()].genre

    def rowCount(self, index):
        return len(self.__genres)

    def addGenre(self, genre: str):
        if not genre:
            return

        existing_genres = [
            existing_genre
            for existing_genre in self.__genres
            if existing_genre.genre == genre
        ]
        if not existing_genres:
            self.__genre_service.add(
                genre, self.__handle_genre_action, self.__handle_failure
            )

    def deleteGenre(self, index: int):
        if index < 0 or index >= len(self.__genres):
            return

        genre = self.__genres[index]

        self.__genre_service.delete(
            genre, self.__handle_none_action, self.__handle_failure
        )

    def __handle_genre_action(self, genre: Genre):
        self.refresh()

    def __handle_none_action(self):
        self.refresh()
