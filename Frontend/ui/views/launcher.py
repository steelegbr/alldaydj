from PySide6.QtWidgets import QMainWindow
from services.logging import LoggingService, Logger
from services.factory import ServiceFactory
from services.settings import SettingsService
from ui.views.generated.launcher import Ui_MainWindow


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
