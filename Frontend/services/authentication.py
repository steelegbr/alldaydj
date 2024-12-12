from enum import StrEnum
from models.dto.api import ApiSettings
from models.dto.authentication import (
    OAuthDeviceCodeRequest,
    OAuthDeviceCodeResponse,
    OAuthError,
    OAuthGrant,
    OAuthScope,
    OAuthTokenRequest,
    OAuthTokenResponse,
    OAuthTokenResponseError,
)
from PySide6.QtCore import QJsonDocument, QTimer
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
    __api_settings: ApiSettings
    __callbacks: List[Callable[[AuthenticationServiceState], None]] = []
    __device_code_response: OAuthDeviceCodeResponse
    __error: Optional[str]
    __logger: Logger
    __state: AuthenticationServiceState
    __timer: QTimer = QTimer()
    __token_response: OAuthTokenResponse

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
        self.__logger.info("Changing state", state=state)
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
            self.__api_settings = api_settings
            self.__logger.info("Retrieved API settings", settings=self.__api_settings)
            self.__request_device_code()

        def failure(error: str, _: str):
            self.__handle_error(f"API Error: {error}")

        self.__api_service.get_api_settings(success, failure)

    def __request_device_code(self):
        self.__set_state(AuthenticationServiceState.DeviceCode)

        url = f"https://{self.__api_settings.auth_domain}/oauth/device/code"
        payload = OAuthDeviceCodeRequest(
            audience=self.__api_settings.auth_audience,
            client_id=self.__api_settings.auth_client_id,
            scope=OAuthScope.OpenIdProfile,
        )

        self.__logger.info("Request device code from OAuth service", url=url)

        def callback(reply: QNetworkReply):
            content = str(reply.readAll().data(), encoding=self.ENCODING)
            if error := reply.error():
                self.__logger.error(
                    "Failed to get Device Code", error=error, response=content
                )
                self.__handle_error(f"Failed to get Device Code")
            else:
                self.__device_code_response = (
                    OAuthDeviceCodeResponse.model_validate_json(content)
                )
                self.__logger.info(
                    "Obtained device code", response=self.__device_code_response
                )
                self.__make_token_request()

        network_access_manager = QNetworkAccessManager()
        network_access_manager.finished.connect(callback)
        network_access_manager.post(
            QNetworkRequest(url), self.__convert_dict_for_post(payload.model_dump())
        )

    def __make_token_request(self, *args, **kwargs):
        self.__set_state(AuthenticationServiceState.AwaitingUserAuth)

        url = url = f"https://{self.__api_settings.auth_domain}/oauth/token"
        payload = OAuthTokenRequest(
            grant_type=OAuthGrant.DeviceCode,
            device_code=self.__device_code_response.device_code,
            client_id=self.__api_settings.auth_client_id,
        )

        self.__logger.info("Request token from OAuth service", url=url)

        def callback(reply: QNetworkReply):
            content = str(reply.readAll().data(), encoding=self.ENCODING)
            if reply.error():
                token_error = OAuthError[OAuthTokenResponseError].model_validate_json(
                    content
                )
                self.__logger.error("Failed to get token", **token_error.model_dump())
                self.__timer.singleShot(
                    self.__device_code_response.interval, self.__make_token_request
                )
            else:
                self.__token_response = OAuthTokenResponse.model_validate_json(content)
                self.__logger.info("Obtained tokens")
                self.__set_state(AuthenticationServiceState.Authenticated)

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

    def register_callback(self, callback: Callable[[AuthenticationServiceState], None]):
        if callback and callback not in self.__callbacks:
            self.__callbacks.append(callback)
            self.__logger.info("Register callback", callback=callback)
        else:
            self.__logger.warning(
                "Asked to register callback that's already registered",
                callback=callback,
            )

    def deregister_callback(
        self, callback: Callable[[AuthenticationServiceState], None]
    ):
        if callback in self.__callbacks:
            self.__callbacks.remove(callback)
            self.__logger.info("Deregister callback", callback=callback)
        else:
            self.__logger.warning(
                "Asked to deregister callback that wasn't registered", callback=callback
            )

    def get_token(self) -> Optional[str]:
        # TODO: Check if the token is still valid and trigger a refresh process in the background
        return self.__token_response.access_token

    def get_device_code(self) -> Optional[str]:
        if self.__device_code_response:
            return self.__device_code_response.device_code

    def get_login_url(self) -> Optional[str]:
        if self.__device_code_response:
            return self.__device_code_response.verification_uri_complete
