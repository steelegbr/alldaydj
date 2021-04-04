from abc import ABC, abstractmethod
from alldaydj.http import Authenticator
from logging import Logger
from requests import get, post
from repositories.generic import MsSqlRepository
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

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
        """
            Retrieves the list of cart types in the repository.

        Returns:
            List[CartType]: The list of cart types.
        """
        pass

    @abstractmethod
    def save(self, cart_type: CartType) -> bool:
        """Saves the cart type to the repository.

        Args:
            cart_type (CartType): The cart type to save.

        Returns:
            bool: An indication if the process was successful.
        """
        return False


class PlayoutOneCartType(Base):
    """
    PlayoutONE implementation of the cart type.
    """

    __tablename__ = "Type"
    ID = Column(Integer, primary_key=True)
    Type = Column(String)
    Billboard = Column(Boolean())


class PlayoutOneCartTypeRepository(CartTypeRepository, MsSqlRepository):
    """
    PlayoutONE implementation of the cart type repository.
    """

    async def get_all(self):
        db_types = self._session.query(PlayoutOneCartType).all()
        types = [CartType(db_type.Type, db_type.Billboard) for db_type in db_types]
        self._logger.info(f"Found {len(types)} cart types.")
        return types

    def save(self, cart_type: CartType) -> bool:
        return False


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
            headers = await self.__authenticator.generate_headers()
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

    async def save(self, cart_type: CartType) -> bool:
        self.__logger.info(
            f"Attempting to add cart type {cart_type.name} to the repository."
        )
        headers = await self.__authenticator.generate_headers()
        data = {"name": cart_type.name, "now_playing": cart_type.now_playing}
        response = post(self.__get_type_url(), data, headers=headers)
        return response.ok