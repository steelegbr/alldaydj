from services.api import ApiService
from services.authentication import AuthenticationService
from services.genre import GenreService
from services.logging import LoggingService, Logger
from services.settings import SettingsService
from services.tag import TagService
from services.type import CartTypeService


class ServiceFactory:
    __authentication_service: AuthenticationService = None
    __logger: Logger = None
    instance = None

    def __new__(cls, logger: Logger = LoggingService().get_logger(__name__)):
        if not cls.instance:
            cls.instance = super(ServiceFactory, cls).__new__(cls)
            cls.instance.__logger = logger
        return cls.instance

    def apiService(self) -> ApiService:
        return ApiService(settings_service=self.settingsService())

    def authenticationService(self) -> AuthenticationService:
        if not self.__authentication_service:
            self.__logger.info("Instantiating Authentication Service")
            self.__authentication_service = AuthenticationService(
                api_service=self.apiService(),
                settings_service=self.settingsService(),
            )
        return self.__authentication_service

    def cartTypeService(self) -> CartTypeService:
        return CartTypeService(
            authetication_service=self.authenticationService(),
            settings_service=self.settingsService(),
        )

    def genreService(self) -> GenreService:
        return GenreService(
            authetication_service=self.authenticationService(),
            settings_service=self.settingsService(),
        )

    def settingsService(self) -> SettingsService:
        return SettingsService()

    def tagService(self) -> TagService:
        return TagService(
            authetication_service=self.authenticationService(),
            settings_service=self.settingsService(),
        )
