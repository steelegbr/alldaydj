from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from urllib.parse import quote_plus, urlencode


class MsSqlRepository:
    """
    Base class for an MS SQL repository.
    """

    _session: Session
    _logger: Logger

    def __init__(
        self, logger: Logger, server: str, database: str, username: str, password: str
    ):
        self._logger = logger
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)
        query = urlencode({"driver": "ODBC Driver 17 for SQL Server"})
        url = f"mssql+pyodbc://{encoded_username}:{encoded_password}@{server}/{database}?{query}"

        logger.info(f"Connecting to MS SQL server at {server}")
        engine = create_engine(url)
        db_session = sessionmaker(bind=engine)
        self._session = db_session()