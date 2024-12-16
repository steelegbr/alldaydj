from PySide6.QtWidgets import QMainWindow, QMessageBox
from pydantic import ValidationError
from services.logging import LoggingService, Logger
from services.factory import ServiceFactory
from services.settings import SettingsService
from ui.views.generated.launcher import Ui_MainWindow
from ui.views.login import Login


class Launcher(QMainWindow, Ui_MainWindow):
    __logger: Logger
    __settings_service: SettingsService

    def __init__(
        self,
        logger: Logger = LoggingService().get_logger(__name__),
        settings_service: SettingsService = ServiceFactory().settingsService(),
    ):
        super().__init__()
        self.setupUi(self)

        self.__logger = logger
        self.__settings_service = settings_service

        settings = self.__settings_service.get()
        self.instanceUrl.setText(str(settings.base_url))

        self.login.clicked.connect(self.handle_login_button_clicked)

    def handle_login_button_clicked(self):
        instance_url = self.instanceUrl.text()
        self.__logger.info("Attempting to set base URL", url=instance_url)

        settings = self.__settings_service.get()
        settings.base_url = instance_url

        try:
            self.__settings_service.save(settings)
            self.__login = Login()
            self.__login.show()
            self.hide()
        except ValidationError:
            self.__logger.error("Base URL not valid", url=instance_url)
            QMessageBox.critical(
                self, "Sorry", "You must enter a valid instance URL to connect to!"
            )
