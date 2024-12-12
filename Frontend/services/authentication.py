from enum import StrEnum
from models.dto.api import ApiSettings
from models.dto.authentication import OAuthDeviceCodeRequest, OAuthDeviceCodeResponse
from PySide6.QtCore import QJsonDocument
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from services.api import ApiService
from services.logging import get_logger, Logger
from typing import Callable, Dict, List, Optional


class AuthenticationServiceState(StrEnum):
    Unauthenticated = "UNAUTHENTICATED"
    Error = "ERROR"
    AuthUrl = "AUTH_URL"
    DeviceCode = "DEVICE_CODE"
    AwaitingUserAuth = "AWAIT_USER_AUTH"
    TimedOut = "TIMED_OUT"
    Authenticated = "AUTHENTICATED"
    RefreshingToken = "REFRESHING_TOKEN"


class AuthenticationService:
    __api_service: ApiService
    __callbacks: List[Callable[[AuthenticationServiceState], None]] = []
    __error: Optional[str]
    __logger: Logger
    __state: AuthenticationServiceState

    ENCODING = "utf-8"

    def __init__(
        self,
        api_service: ApiService = None,
        logger: Logger = get_logger(__name__),
        state: AuthenticationServiceState = AuthenticationServiceState.Unauthenticated,
    ):
        self.__api_service = api_service
        self.__logger = logger
        self.__state = state

    def get_state(self) -> AuthenticationServiceState:
        return self.__state

    def __set_state(self, state: AuthenticationServiceState):
        self.__logger("Changing state", state=state)
        self.__state = state
        for callback in self.__callbacks:
            callback(state)

    def authenticate(self):
        if self.get_state() in [
            AuthenticationServiceState.Error,
            AuthenticationServiceState.Unauthenticated,
        ]:
            # Start the authentication process
            self.__get_auth_url()
        else:
            self.__logger.warning(
                "Can't attempt authentication in current state",
                state=self.get_state(),
            )

    def __get_auth_url(self):
        self.__set_state(AuthenticationServiceState.AuthUrl)
        self.__error = None

        def success(api_settings: ApiSettings):
            self.__request_device_code(api_settings)

        def failure(error: str, _: str):
            self.__handle_error(f"API Error: {error}")

        self.__api_service.get_api_settings(success, failure)

    def __request_device_code(self, api_settings: ApiSettings):
        self.__set_state(AuthenticationServiceState.DeviceCode)

        url = f"https://{api_settings.auth_domain}/oauth/device/code"
        payload = OAuthDeviceCodeRequest(
            audience=api_settings.auth_audience,
            client_id=api_settings.auth_client_id,
        )

        def callback(reply: QNetworkReply):
            content = str(reply.readAll().data(), encoding=self.ENCODING)
            if error := reply.error():
                self.__logger.error(
                    "Failed to get Device Code", error=error, response=content
                )
                self.__handle_error(f"Failed to get Device Code")
            else:
                response = OAuthDeviceCodeResponse.model_validate(content)
                self.__logger.info("Obtained device code", response=response)

        network_access_manager = QNetworkAccessManager()
        network_access_manager.finished.connect(callback)
        network_access_manager.post(
            QNetworkRequest(url), self.__convert_dict_for_post(payload.model_dump())
        )

    def __convert_dict_for_post(self, payload: Dict):
        doc = QJsonDocument(payload)
        return doc.toJson()

    def __handle_error(self, error: str):
        self.__set_state(AuthenticationServiceState.Error)
        self.__error = error

    def get_error(self) -> Optional[str]:
        return self.__error
