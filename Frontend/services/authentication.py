from enum import StrEnum
from services.logging import get_logger, Logger
from typing import Callable, List, Optional


class AuthenticationServiceState(StrEnum):
    Unauthenticated = "UNAUTHENTICATED"
    Error = "ERROR"
    DeviceCode = "DEVICE_CODE"
    AwaitingUserAuth = "AWAIT_USER_AUTH"
    TimedOut = "TIMED_OUT"
    Authenticated = "AUTHENTICATED"
    RefreshingToken = "REFRESHING_TOKEN"


class AuthenticationService:
    __callbacks: List[Callable[[AuthenticationServiceState], None]] = []
    __error: Optional[str]
    __logger: Logger
    __state: AuthenticationServiceState

    def __init__(
        self,
        logger: Logger = get_logger(__name__),
        state: AuthenticationServiceState = AuthenticationServiceState.Unauthenticated,
    ):
        self.__logger = logger
        self.__state = state

    def get_state(self) -> AuthenticationServiceState:
        return self.__state

    def __set_state(self, state: AuthenticationServiceState):
        self.__logger("Setting state to %s", state=state)
        self.__state = state
        for callback in self.__callbacks:
            callback(state)

    def authenticate(self):
        if self.get_state() in [
            AuthenticationServiceState.Error,
            AuthenticationServiceState.Unauthenticated,
        ]:
            # Get a device code
            pass
        else:
            self.__logger.warning(
                "Can't attempt authentication when in the %s state",
                state=self.get_state(),
            )
