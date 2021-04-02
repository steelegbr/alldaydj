from abc import ABC, abstractmethod
from alldaydj.http import Authenticator
from logging import Logger
from requests import get
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

    async def get_all(self):
        db_types = self._session.query(PlayoutOneCartType).all()
        types = [CartType(db_type.Type, db_type.Billboard) for db_type in db_types]
        self._logger.info(f"Found {len(types)} cart types.")
        return types


class AllDayDjCartTypeRepository(CartTypeRepository):

    __authenticator: Authenticator
    __logger: Logger
    __base_url: str
    __secure: bool

    def __init__(
        self, authenticator: Authenticator, logger: Logger, base_url: str, secure: bool
    ):
        self.__authenticator = authenticator
        self.__logger = logger
        self.__base_url = base_url
        self.__secure = secure

    def __get_type_url(self) -> str:
        """
            Gets the URL to list from and add cart types to.

        Returns:
            str: The URL.
        """
        if self.__secure:
            return f"https://{self.__base_url}/api/type/"
        return f"http://{self.__base_url}/api/type/"

    async def get_all(self):
        cart_types = []

        next_url = self.__get_type_url()
        while next_url:
            headers = {
                "Authorization": f"Bearer {await self.__authenticator.get_token()}"
            }
            response = get(next_url, headers=headers)
            if response.ok:
                response_json = response.json()
                json_results = response_json.get("results", [])
                cart_types += [
                    CartType(cart_type["name"], cart_type["now_playing"])
                    for cart_type in json_results
                ]
                self.__logger.info(
                    f"Found {len(json_results)} cart types at {next_url}"
                )
                next_url = response_json["next"]
            else:
                self.__logger.error(
                    f"Error code {response.status_code} getting cart types from {next_url}"
                )
                next_url = None

        return cart_types
