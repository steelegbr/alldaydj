from abc import ABC, abstractmethod
from logging import Logger
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from urllib.parse import quote_plus, urlencode

Base = declarative_base()


class CartType:
    """
    Specifies a type of cart the system can know about.
    """

    _name: str
    _now_playing: bool

    def __init__(self, name: str, now_playing: bool):
        self._name = name
        self._now_playing = now_playing

    @property
    @abstractmethod
    def name(self) -> str:
        """
            Gets the name of the cart type.

        Returns:
            str: The name of the cart type.
        """
        return self._name

    @property
    @abstractmethod
    def now_playing(self) -> bool:
        """
            Indicates if the type should appear in now playing.

        Returns:
            bool: TRUE if it should.
        """
        return self._now_playing


class CartTypeRepository(ABC):
    """
    Repository for holding cart types.
    """

    @abstractmethod
    def get_all(self) -> List[CartType]:
        pass


class PlayoutOneCartType(Base):
    """
    PlayoutONE implementation of the cart type.
    """

    __tablename__ = "Type"
    ID = Column(Integer, primary_key=True)
    Type = Column(String)
    Billboard = Column(Boolean())


class PlayoutOneCartTypeRepository(CartTypeRepository):
    """
    PlayoutONE implementation of the cart type repository.
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

    def get_all(self):
        db_types = self._session.query(PlayoutOneCartType).all()
        types = [CartType(db_type.Type, db_type.Billboard) for db_type in db_types]
        self._logger.info(f"Found {len(types)} cart types.")
        return types
