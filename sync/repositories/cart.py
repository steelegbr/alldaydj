from abc import ABC, abstractmethod
from alldaydj.http import Authenticator
from logging import Logger
from requests import get, post
from repositories.cart_type import PlayoutOneCartType
from repositories.generic import AllDayDjRepository, MsSqlRepository
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import List
from urllib.parse import quote_plus, urlencode

Base = declarative_base()


class Cart:
    """Specifies a cart that has audio attached."""

    __label: str
    __title: str
    __display_artist: str
    __artists: List[str]
    __cue_audio_start: int
    __cue_audio_end: int
    __cue_intro_start: int
    __cue_intro_end: int
    __cue_segue: int
    __sweeper: bool
    __year: int
    __isrc: str
    __composer: str
    __publisher: str
    __record_label: str
    __tags: List[str]
    __cart_type: str
    __internal_id: str
    __fade: bool

    def __init__(
        self,
        label: str,
        title: str,
        display_artist: str,
        artists: List[str],
        cue_audio_start: int,
        cue_audio_end: int,
        cue_intro_start: int,
        cue_intro_end: int,
        cue_segue: int,
        sweeper: bool,
        year: int,
        isrc: str,
        composer: str,
        publisher: str,
        record_label: str,
        tags: List[str],
        cart_type: str,
        internal_id: str,
        fade: bool,
    ):
        self.__label = label
        self.__title = title
        self.__display_artist = display_artist
        self.__artists = artists
        self.__cue_audio_start = cue_audio_start
        self.__cue_audio_end = cue_audio_end
        self.__cue_intro_start = cue_intro_start
        self.__cue_intro_end = cue_intro_end
        self.__cue_segue = cue_segue
        self.__sweeper = sweeper
        self.__year = year
        self.__isrc = isrc
        self.__composer = composer
        self.__publisher = publisher
        self.__record_label = record_label
        self.__tags = tags
        self.__cart_type = cart_type
        self.__internal_id = internal_id
        self.__fade = fade

    @property
    def label(self) -> str:
        return self.__label

    @property
    def title(self) -> str:
        return self.__title

    @property
    def display_artist(self) -> str:
        return self.__display_artist

    @property
    def artists(self) -> str:
        return self.__artists

    @property
    def cue_audio_start(self) -> int:
        return self.__cue_audio_start

    @property
    def cue_audio_end(self) -> int:
        return self.__cue_audio_end

    @property
    def cue_intro_start(self) -> int:
        return self.__cue_intro_start

    @property
    def cue_intro_end(self) -> int:
        return self.__cue_intro_end

    @property
    def cue_segue(self) -> str:
        return self.__cue_segue

    @property
    def title(self) -> str:
        return self.__title

    @property
    def sweeper(self) -> bool:
        return self.__sweeper

    @property
    def year(self) -> int:
        return self.__year

    @property
    def isrc(self) -> str:
        return self.__isrc

    @property
    def composer(self) -> str:
        return self.__composer

    @property
    def publisher(self) -> str:
        return self.__publisher

    @property
    def record_label(self) -> str:
        return self.__record_label

    @property
    def cart_type(self) -> str:
        return self.__cart_type

    @property
    def internal_id(self) -> str:
        return self.__internal_id

    @property
    def fade(self) -> bool:
        return self.__fade


class CartRepository:
    """Repository for holding cart data."""

    @abstractmethod
    async def get_all(self) -> List[Cart]:
        """Obtains the list of all carts in the repository.

        Returns:
            List[Cart]: The list of carts.
        """
        pass

    @abstractmethod
    async def get_by_label(self, label: str) -> Cart:
        """Searches for a cart by the label.

        Args:
            label (str): The label to search by.

        Returns:
            Cart: The cart, if it exists.
        """
        pass

    async def save_new(self, cart: Cart) -> bool:
        """Saves a new cart to the respository.

        Args:
            cart (Cart): The cart to save.

        Returns:
            bool: An indication if the process was successful or not.
        """
        pass

    async def update(self, cart: Cart, existing_cart: Cart) -> bool:
        """Updates an existing cart in the repository.

        Args:
            cart (Cart): The new information to add to the cart.
            existing_cart (Cart): The existing cart in the database.

        Returns:
            bool: [description]
        """
        pass


class PlayoutOneCart(Base):
    """
    PlayoutONE implementation of the cart.
    """

    __tablename__ = "Audio"
    ID = Column(Integer, primary_key=True)
    UID = Column(String)
    Title = Column(String)
    Artist = Column(String)
    TrimIn = Column(Integer)
    Intro = Column(Integer)
    Extro = Column(Integer)
    TrimOut = Column(Integer)
    Oversweep = Column(Boolean)
    AudioYear = Column(Integer)
    Type_id = Column("Type", Integer, ForeignKey(PlayoutOneCartType.ID))
    Type = relationship(PlayoutOneCartType)
    Fade = Column(Boolean)


class PlayoutOneCartRepository(CartRepository, MsSqlRepository):
    """
    PlayoutONE implementation of the cart repository.
    """

    async def get_all(self):
        db_carts = self._session.query(PlayoutOneCart).join(PlayoutOneCartType).all()
        carts = [
            Cart(
                db_cart.UID,
                db_cart.Title,
                db_cart.Artist,
                [],
                db_cart.TrimIn,
                db_cart.TrimOut,
                db_cart.TrimIn,
                db_cart.Intro,
                db_cart.Extro,
                db_cart.Oversweep,
                db_cart.AudioYear,
                None,
                None,
                None,
                None,
                [],
                db_cart.Type.Type,
                db_cart.ID,
                db_cart.Fade,
            )
            for db_cart in db_carts
        ]
        self._logger.info(f"Found {len(carts)} cart(s).")
        return carts


class AllDayDjCartRepository(CartRepository, AllDayDjRepository):
    def __post_cart_url(self) -> str:
        """
            Gets the URL to post a cart to.

        Returns:
            str: The URL to post new carts to.
        """
        if self._secure:
            return f"https://{self._base_url}/api/cart/"
        return f"http://{self._base_url}/api/cart/"

    def __get_cart_url_by_label(self, label: str) -> str:
        """
            Gets the URL for a cart based on its label.

        Args:
            label (str): The cart label.

        Returns:
            str: The URL.
        """
        if self._secure:
            return f"https://{self._base_url}/api/cart/by-label/{label}/"
        return f"http://{self._base_url}/api/cart/by-label/{label}/"

    async def get_by_label(self, label: str):
        url = self.__get_cart_url_by_label(label)
        self._logger.info(f"Retrieving cart {label} from AllDay DJ.")

        headers = await self._authenticator.generate_headers()
        response = get(url, headers=headers)

        if response.ok:
            self._logger.info(f"Successfully retrieved cart {label} from AllDay DJ.")
            return response.json()
        self._logger.info(f"Failed to retrieve cart {label} from AllDay DJ.")

    async def save_new(self, cart: Cart):
        self._logger.info(f"Attempting to add cart {cart.label} to the repository.")
        headers = await self._authenticator.generate_headers()
        data = {
            "label": cart.label,
            "title": cart.title,
            "display_artist": cart.display_artist,
            "cue_audio_start": cart.cue_audio_start,
            "cue_audio_end": cart.cue_audio_end,
            "cue_intro_start": cart.cue_intro_start,
            "cue_intro_end": cart.cue_intro_end,
            "cue_segue": cart.cue_segue,
            "sweeper": cart.sweeper,
            "year": cart.year,
            "isrc": cart.isrc,
            "composer": cart.composer,
            "publisher": cart.publisher,
            "record_label": cart.record_label,
            "type": cart.cart_type,
            "fade": cart.fade,
        }
        response = post(self.__post_cart_url(), data, headers=headers)
        if response.ok:
            self._logger.info(
                f"Successfully added cart {cart.label} to the repository."
            )
        else:
            self._logger.error(
                f"Error code {response.status_code} adding cart {cart.label} to the repository."
            )
        return response.ok or False
