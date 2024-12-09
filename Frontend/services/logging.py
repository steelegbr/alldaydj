from logging import Logger
from structlog import get_logger


class LoggingService:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(LoggingService, cls).__new__(cls)
        return cls.instance

    def get_logger(self, name: str) -> Logger:
        return get_logger(name)
