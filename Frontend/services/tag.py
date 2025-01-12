from models.dto.api import Pagination
from models.dto.audio import Tag
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply
from services.authentication import AuthenticationService
from services.logging import LoggingService, Logger
from services.settings import SettingsService
from typing import Callable, List
from urllib.parse import urljoin


class TagService:
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
        success: Callable[[List[Tag]], None],
        failure: Callable[[List[str]], None],
        tags_so_far: List[Tag],
    ):
        self.__logger.info("GET Tags request", url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "GET Tags request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to retrieve tags from server")
            else:
                self.__logger.info("GET Tags request successful", url=url)
                page_of_results = Pagination[Tag].model_validate_json(content)
                tags_so_far.extend(page_of_results.items)
                if page_of_results.pages > page_of_results.page:
                    self.__get_page(
                        page_of_results.next, page + 1, success, failure, tags_so_far
                    )
                else:
                    success(tags_so_far)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.get(
            self.__authentication_service.get_authenticated_request(url)
        )

    def get_all_tags(
        self, success: Callable[[List[Tag]], None], failure: Callable[[str], None]
    ):
        url = urljoin(str(self.__settings_service.get().base_url), "/api/tag")
        self.__get_page(url, 1, success, failure, [])

    def add_tag(
        self, tag: str, success: Callable[[Tag], None], failure: Callable[[str], None]
    ):
        url = urljoin(str(self.__settings_service.get().base_url), "/api/tag")
        body = Tag(tag=tag)
        self.__logger.info("POST Tag Request", body=body, url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "POST Tag request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to create the tag")
            else:
                self.__logger.info("POST Tag request successful", url=url)
                tag = Tag.model_validate_json(content)
                success(tag)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.post()
