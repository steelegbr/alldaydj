from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QMainWindow
from services.authentication import AuthenticationService, AuthenticationServiceState
from services.factory import ServiceFactory
from typing import Dict
from ui.views.generated.login import Ui_MainWindow
from ui.views.main import MainScreen
from webbrowser import open as open_webbrowser

LOGIN_STATUS_MAP: Dict[AuthenticationServiceState, str] = {
    AuthenticationServiceState.Authenticated: "",
    AuthenticationServiceState.AuthUrl: "Obtaining authentication URL...",
    AuthenticationServiceState.AwaitingUserAuth: "Please confirm the code below and log in.",
    AuthenticationServiceState.DeviceCode: "Obtaining device code...",
    AuthenticationServiceState.Error: "Something went wrong!",
    AuthenticationServiceState.RefreshingToken: "Refreshing out of date token...",
    AuthenticationServiceState.TimedOut: "Sorry, you took too long to log in. Please try again.",
    AuthenticationServiceState.Unauthenticated: "",
}


class Login(QMainWindow, Ui_MainWindow):
    __authentication_service: AuthenticationService
    __main_screen: MainScreen = None

    def __init__(
        self,
        authentication_service: AuthenticationService = ServiceFactory().authenticationService(),
    ):
        super().__init__()
        self.setupUi(self)

        movie = QMovie("./ui/assets/throbber.gif")
        movie.setScaledSize(self.throbber.size())
        self.throbber.setMovie(movie)
        movie.start()
        self.throbber.show()

        self.__authentication_service = authentication_service
        self.__authentication_service.register_callback(
            self.__handle_auth_status_change
        )
        self.__authentication_service.authenticate()

    def __handle_auth_status_change(self, state: AuthenticationServiceState):
        self.status.setText(LOGIN_STATUS_MAP[state])
        self.code.setText("")

        match state:
            case AuthenticationServiceState.AwaitingUserAuth:
                self.code.setText(self.__authentication_service.get_user_code())
                open_webbrowser(self.__authentication_service.get_login_url())
            case AuthenticationServiceState.Authenticated:
                if self.__main_screen is None:
                    self.__main_screen = MainScreen()
                self.__main_screen.show()
                self.hide()
