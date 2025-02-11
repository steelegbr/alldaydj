from models.dto.api import Pagination
from models.dto.audio import Genre
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply
from services.authentication import AuthenticationService
from services.json import JsonService
from services.logging import LoggingService, Logger
from services.settings import SettingsService
from typing import Callable, List
from urllib.parse import urljoin


class GenreService:
    __authentication_service: AuthenticationService
    __logger: Logger
    __settings_service: SettingsService
    __network_access_manager: QNetworkAccessManager

    ENCODING = "utf-8"

    def __init__(
        self,
        authetication_service: AuthenticationService = None,
        logger: Logger = LoggingService().get_logger(__name__),
        settings_service: SettingsService = None,
    ):
        self.__authentication_service = authetication_service
        self.__logger = logger
        self.__network_access_manager = QNetworkAccessManager()
        self.__settings_service = settings_service

    def __get_page(
        self,
        url: str,
        page: int,
        success: Callable[[List[Genre]], None],
        failure: Callable[[List[Genre]], None],
        genres_so_far: List[Genre],
    ):
        self.__logger.info("GET Genres request", url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "GET Genres request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to retrieve genres from server")
            else:
                self.__logger.info("GET Genres request successful", url=url)
                page_of_results = Pagination[Genre].model_validate_json(content)
                genres_so_far.extend(page_of_results.items)
                if page_of_results.pages > page_of_results.page:
                    self.__get_page(
                        page_of_results.next, page + 1, success, failure, genres_so_far
                    )
                else:
                    success(genres_so_far)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.get(
            self.__authentication_service.get_authenticated_request(url)
        )

    def get_all(
        self, success: Callable[[List[Genre]], None], failure: Callable[[str], None]
    ):
        url = urljoin(str(self.__settings_service.get().base_url), "/api/genre")
        self.__get_page(url, 1, success, failure, [])

    def add(
        self,
        cart_type: str,
        success: Callable[[Genre], None],
        failure: Callable[[str], None],
    ):
        url = urljoin(str(self.__settings_service.get().base_url), "/api/genre")
        body = Genre(id=None, cart_type=cart_type)
        self.__logger.info("POST Genre Request", body=body, url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "POST Genre request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to create the genre")
            else:
                self.__logger.info("POST Genre request successful", url=url)
                genre = Genre.model_validate_json(content)
                success(genre)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.post(
            self.__authentication_service.get_authenticated_request(url),
            JsonService.dict_to_json(body.model_dump(exclude_none=True)),
        )

    def delete(
        self, genre: Genre, success: Callable[[], None], failure: Callable[[str], None]
    ):
        url = urljoin(
            str(self.__settings_service.get().base_url), f"/api/genre/{genre.id}"
        )
        self.__logger.info("DELETE Genre Request", url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "DELETE Genre request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to delete the cart type")
            else:
                self.__logger.info("DELETE Genre request successful", url=url)
                success()

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.deleteResource(
            self.__authentication_service.get_authenticated_request(url)
        )
