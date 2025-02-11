from models.dto.api import Pagination
from models.dto.audio import CartType
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply
from services.authentication import AuthenticationService
from services.json import JsonService
from services.logging import LoggingService, Logger
from services.settings import SettingsService
from typing import Callable, List
from urllib.parse import urljoin


class CartTypeService:
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
        success: Callable[[List[CartType]], None],
        failure: Callable[[List[CartType]], None],
        cart_types_so_far: List[CartType],
    ):
        self.__logger.info("GET Cart Types request", url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "GET Cart Types request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to retrieve cart types from server")
            else:
                self.__logger.info("GET Cart Types request successful", url=url)
                page_of_results = Pagination[CartType].model_validate_json(content)
                cart_types_so_far.extend(page_of_results.items)
                if page_of_results.pages > page_of_results.page:
                    self.__get_page(
                        page_of_results.next, page + 1, success, failure, cart_types_so_far
                    )
                else:
                    success(cart_types_so_far)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.get(
            self.__authentication_service.get_authenticated_request(url)
        )

    def get_all(
        self, success: Callable[[List[CartType]], None], failure: Callable[[str], None]
    ):
        url = urljoin(str(self.__settings_service.get().base_url), "/api/type")
        self.__get_page(url, 1, success, failure, [])

    def add(
        self,
        cart_type: str,
        success: Callable[[CartType], None],
        failure: Callable[[str], None],
    ):
        url = urljoin(str(self.__settings_service.get().base_url), "/api/type")
        body = CartType(id=None, cart_type=cart_type)
        self.__logger.info("POST Cart Type Request", body=body, url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "POST Cart Type request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to create the tag")
            else:
                self.__logger.info("POST Cart Type request successful", url=url)
                cart_type = CartType.model_validate_json(content)
                success(cart_type)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.post(
            self.__authentication_service.get_authenticated_request(url),
            JsonService.dict_to_json(body.model_dump(exclude_none=True)),
        )

    def delete(
        self,
        cart_type: CartType,
        success: Callable[[], None],
        failure: Callable[[str], None],
    ):
        url = urljoin(
            str(self.__settings_service.get().base_url), f"/api/type/{cart_type.id}"
        )
        self.__logger.info("DELETE Cart Type Request", url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NoError:
                self.__logger.error(
                    "DELETE Cart Type request failed",
                    url=url,
                    error=reply.error(),
                    response=content,
                )
                failure("Failed to delete the cart type")
            else:
                self.__logger.info("DELETE Cart Type request successful", url=url)
                success()

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.deleteResource(
            self.__authentication_service.get_authenticated_request(url)
        )
