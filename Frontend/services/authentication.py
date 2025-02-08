from datetime import datetime, timezone
from enum import StrEnum
from jwt import decode
from models.dto.api import ApiSettings
from models.dto.authentication import (
    OAuthDeviceCodeRequest,
    OAuthDeviceCodeResponse,
    OAuthError,
    OAuthGrant,
    OAuthScope,
    OAuthRefreshRequest,
    OAuthRefreshResponse,
    OAuthTokenRequest,
    OAuthTokenResponse,
    OAuthTokenResponseError,
)
from PySide6.QtCore import QTimer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from services.api import ApiService
from services.json import JsonService
from services.logging import get_logger, Logger
from services.settings import SettingsService
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
    __access_token: str
    __api_service: ApiService
    __api_settings: ApiSettings
    __callbacks: List[Callable[[AuthenticationServiceState], None]] = []
    __device_code_response: OAuthDeviceCodeResponse
    __error: Optional[str]
    __logger: Logger
    __network_access_manager: QNetworkAccessManager
    __refresh_token: str
    __settings_service: SettingsService
    __state: AuthenticationServiceState
    __timer: QTimer = QTimer()

    ENCODING = "utf-8"

    def __init__(
        self,
        api_service: ApiService = None,
        logger: Logger = get_logger(__name__),
        settings_service: SettingsService = None,
        state: AuthenticationServiceState = AuthenticationServiceState.Unauthenticated,
    ):
        self.__api_service = api_service
        self.__logger = logger
        self.__network_access_manager = QNetworkAccessManager()
        self.__settings_service = settings_service
        self.__state = state
        self.__refresh_token_from_settings()

    def get_state(self) -> AuthenticationServiceState:
        return self.__state

    def __set_state(self, state: AuthenticationServiceState):
        if self.get_state() is state:
            return

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

            if self.__refresh_token:
                self.do_refresh_token(self.__refresh_token)
            else:
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
            scope=OAuthScope.OpenIdProfileWithOfflineAccess,
        )

        self.__logger.info(
            "Request device code from OAuth service",
            url=url,
        )

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NetworkError.NoError:
                self.__logger.error(
                    "Failed to get Device Code", error=reply.error(), response=content
                )
                self.__handle_error("Failed to get Device Code")
            else:
                self.__device_code_response = (
                    OAuthDeviceCodeResponse.model_validate_json(content)
                )
                self.__logger.info(
                    "Obtained device code", response=self.__device_code_response
                )
                self.__make_token_request()

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.post(
            JsonService.generate_json_request(url),
            JsonService.dict_to_json(payload.model_dump()),
        )

    def __make_token_request(self, *args, **kwargs):
        self.__set_state(AuthenticationServiceState.AwaitingUserAuth)

        url = f"https://{self.__api_settings.auth_domain}/oauth/token"
        payload = OAuthTokenRequest(
            grant_type=OAuthGrant.DeviceCode,
            device_code=self.__device_code_response.device_code,
            client_id=self.__api_settings.auth_client_id,
        )

        self.__logger.info("Request token from OAuth service", url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NetworkError.NoError:
                token_error = OAuthError[OAuthTokenResponseError].model_validate_json(
                    content
                )

                if token_error.error in [
                    OAuthTokenResponseError.AuthorizationPending,
                    OAuthTokenResponseError.SlowDown,
                ]:
                    self.__timer.singleShot(
                        self.__device_code_response.interval * 1000,
                        self.__make_token_request,
                    )
                else:
                    self.__logger.warning(
                        "Failed to get token", **token_error.model_dump()
                    )
                    self.__set_state(AuthenticationServiceState.Error)

            else:
                token_response = OAuthTokenResponse.model_validate_json(content)
                self.__access_token = token_response.access_token
                self.__set_refresh_token(token_response.refresh_token)

                self.__logger.info(
                    "Obtained tokens", expires_in=token_response.expires_in
                )
                self.__set_state(AuthenticationServiceState.Authenticated)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.post(
            JsonService.generate_json_request(url),
            JsonService.dict_to_json(payload.model_dump()),
        )

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

    def is_token_still_valid(self, token: str, refresh_hours: int = 1):
        decoded = decode(token, options={"verify_signature": False})
        expiry_time = datetime.fromtimestamp(decoded["exp"], timezone.utc)
        now = datetime.now(timezone.utc)

        difference = expiry_time - now
        return (difference.total_seconds() // 3600) > refresh_hours

    def do_refresh_token(self, refresh_token: Optional[str] = None):
        self.__set_state(AuthenticationServiceState.RefreshingToken)

        if not refresh_token:
            refresh_token = self.__refresh_token

        url = f"https://{self.__api_settings.auth_domain}/oauth/token"
        payload = OAuthRefreshRequest(
            client_id=self.__api_settings.auth_client_id,
            grant_type=OAuthGrant.RefreshToken,
            refresh_token=refresh_token,
        )

        self.__logger.info("Refresh token from OAuth service", url=url)

        def callback(reply: QNetworkReply):
            self.__network_access_manager.finished.disconnect(callback)
            content = str(reply.readAll().data(), encoding=self.ENCODING)

            if reply.error() is not QNetworkReply.NetworkError.NoError:
                self.__logger.warning("Failed to refresh token", error=reply.readAll())
                self.__set_state(AuthenticationServiceState.Unauthenticated)
                self.__clear_refresh_token()
                self.authenticate()

            else:
                refresh_response = OAuthRefreshResponse.model_validate_json(content)
                self.__access_token = refresh_response.access_token

                self.__logger.info(
                    "Refreshed token", expires_in=refresh_response.expires_in
                )
                self.__set_state(AuthenticationServiceState.Authenticated)

        self.__network_access_manager.finished.connect(callback)
        self.__network_access_manager.post(
            JsonService.generate_json_request(url),
            JsonService.dict_to_json(payload.model_dump()),
        )

    def get_token(self) -> Optional[str]:
        if not self.__access_token:
            return

        if (
            self.get_state() is AuthenticationServiceState.Authenticated
            and not self.is_token_still_valid(self.__access_token)
        ):
            self.do_refresh_token(None)

        return self.__access_token

    def get_authenticated_request(self, url: str) -> QNetworkRequest:
        request = QNetworkRequest()
        request.setUrl(url)
        request.setRawHeader(b"Authorization", f"Bearer {self.get_token()}".encode())
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        return request

    def get_user_code(self) -> Optional[str]:
        if self.__device_code_response:
            return self.__device_code_response.user_code

    def get_login_url(self) -> Optional[str]:
        if self.__device_code_response:
            return self.__device_code_response.verification_uri_complete

    def set_api_settings(self, api_settings: ApiSettings):
        self.__api_settings = api_settings
        self.__logger.info("Set API settings", settings=self.__api_settings)

    def __set_refresh_token(self, refresh_token: str):
        self.__logger.info("Set refresh token")
        self.__refresh_token = refresh_token

        settings = self.__settings_service.get()
        settings.refresh_token = refresh_token
        self.__settings_service.save(settings)

    def __refresh_token_from_settings(self):
        settings = self.__settings_service.get()
        self.__refresh_token = settings.refresh_token

    def __clear_refresh_token(self):
        self.__logger.info("Clear refresh token")
        settings = self.__settings_service.get()
        settings.refresh_token = None
        self.__settings_service.save(settings)
        self.__refresh_token = None
