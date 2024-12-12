from models.core.settings import Settings
from pydantic import HttpUrl
from PySide6.QtCore import QCoreApplication, QSettings
from services.logging import Logger, LoggingService


class SettingsService:
    __logger: Logger
    __settings: QSettings

    ORG_NAME = "Solid Radio"
    ORG_DOMAIN = "solidradio.co.uk"
    APP_NAME = "AllDay DJ"

    def __init__(self, logger: Logger = LoggingService().get_logger(__name__)):
        self.__logger = logger
        self.__logger.info(
            "Instantiating Settings Service",
            organisaton=self.ORG_DOMAIN,
            domain=self.ORG_DOMAIN,
            application=self.APP_NAME,
        )

        QCoreApplication.setOrganizationName(self.ORG_NAME)
        QCoreApplication.setOrganizationDomain(self.ORG_DOMAIN)
        QCoreApplication.setApplicationName(self.APP_NAME)
        self.__settings = QSettings()

    def __map_key_to_value(self, key: str, default):
        return self.__settings.value(key, default)

    def __map_value_for_save(self, value):
        match value:
            case HttpUrl():
                return str(value)
            case _:
                return value

    def get(self) -> Settings:
        settings_dict = Settings().model_dump()
        for key in settings_dict.keys():
            settings_dict[key] = self.__map_key_to_value(key, settings_dict[key])

        self.__logger.debug("Extracted settings", settings=settings_dict)
        return Settings.model_validate(settings_dict)

    def save(self, settings: Settings):
        if not settings:
            self.__logger.error("Cannot save settings as no settings supplied!")
            return

        settings_dict = settings.model_dump()
        for key in settings_dict.keys():
            self.__settings.setValue(key, self.__map_value_for_save(settings_dict[key]))
        self.__logger.info("Saved settings")
