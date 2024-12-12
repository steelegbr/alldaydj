from models.dto.api import ApiSettings
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from services.logging import LoggingService, Logger
from services.settings import SettingsService
from typing import Callable
from urllib.parse import urljoin


class ApiService:
    __logger: Logger
    __settings_service: SettingsService

    ENCODING = "utf-8"

    def __init__(
        self,
        logger: Logger = LoggingService().get_logger(__name__),
        settings_service: SettingsService = None,
    ):
        self.__logger = logger
        self.__settings_service = settings_service

    def __get_request_unauthenticated(
        self,
        url: str,
        success: Callable[[str], None],
        failure: Callable[[QNetworkReply.NetworkError, str], None],
    ):
        network_access_manager = QNetworkAccessManager()

        def callback(reply: QNetworkReply):
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if error := reply.error():
                self.__logger.error(
                    "Network error encountered",
                    url=url,
                    body=reply.readAll(),
                    error=error,
                )
                failure(error, content)
            else:
                self.__logger.info("Successful network request", url=url)
                success(content)

        network_access_manager.finished.connect(callback)
        network_access_manager.get(QNetworkRequest(url))

    def get_api_settings(
        self,
        success: Callable[[ApiSettings], None],
        failure: Callable[[QNetworkReply.NetworkError, str], None],
    ):
        url = urljoin(str(self.__settings_service.get().base_url), "/api/settings")
        self.__logger.info("GET API Settings request", url=url)

        def success_mapper(content: str):
            success(ApiSettings.model_validate_json(content))

        self.__get_request_unauthenticated(url, success_mapper, failure)
