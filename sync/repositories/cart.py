from abc import ABC, abstractmethod
from alldaydj.http import Authenticator
from logging import Logger
from pathlib import Path
from requests import get, patch, post
from repositories.cart_type import PlayoutOneCartType
from repositories.generic import AllDayDjRepository, MsSqlRepository
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import List, Dict
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

    @property
    def tags(self) -> List[str]:
        return self.__tags


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

    async def update(self, differences: Dict, cart_id: str) -> bool:
        """Updates an existing cart in the repository.

        Args:
            differences (Dict): The new information to add to the cart.
            cart_id (str): The ID of the cart in the destination database.

        Returns:
            bool: [description]
        """
        pass

    @staticmethod
    def cart_to_dictionary(cart: Cart) -> dict:
        """Translates a cart object into a dictionary.

        Args:
            cart (Cart): The cart to translate.

        Returns:
            dict: The translated cart.
        """
        return {
            "label": cart.label,
            "title": cart.title or "",
            "display_artist": cart.display_artist or "",
            "cue_audio_start": cart.cue_audio_start,
            "cue_audio_end": cart.cue_audio_end,
            "cue_intro_start": cart.cue_intro_start,
            "cue_intro_end": cart.cue_intro_end,
            "cue_segue": cart.cue_segue,
            "sweeper": cart.sweeper,
            "year": int(cart.year) if cart.year else 0,
            "isrc": cart.isrc,
            "composer": cart.composer,
            "publisher": cart.publisher,
            "record_label": cart.record_label,
            "type": cart.cart_type,
            "fade": cart.fade,
            "tags": cart.tags or [],
            "artists": cart.artists or [],
        }

    @abstractmethod
    def get_file_path(self, cart: Cart) -> str:
        """
            Obtains the file path for a given cart.

        Args:
            cart (Cart): The cart to get the file path for.

        Returns:
            Path: The file path.
        """
        pass

    @abstractmethod
    async def upload_audio(self, cart_id: str, file_path: Path) -> bool:
        """
            Uploads a given audio file to the repository.

        Args:
            cart_id (str): The cart we matched on to.
            file_path (Path): The file to be upload.

        Returns:
            bool: A flag indicating if the process was successful
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

    __file_path: str
    EXPECTED_FILE_TYPES = [".WAV", ".wav", ".MP3", ".mp3"]

    def __init__(
        self,
        logger: Logger,
        server: str,
        database: str,
        username: str,
        password: str,
        file_path: str,
    ):
        self.__file_path = file_path
        super(PlayoutOneCartRepository, self).__init__(
            logger, server, database, username, password
        )

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

    def get_file_path(self, cart: Cart) -> str:
        base_path = Path(self.__file_path)
        for file_type in self.EXPECTED_FILE_TYPES:
            path = base_path / f"{cart.label}{file_type}"
            if path.exists():
                return path


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

    def __get_cart_url_by_id(self, cart_id: str) -> str:
        """
            Gets the URL for a cart based on its ID.

        Args:
            cart_id (str): The ID for the cart.

        Returns:
            str: The URL.
        """
        if self._secure:
            return f"https://{self._base_url}/api/cart/{cart_id}/"
        return f"http://{self._base_url}/api/cart/{cart_id}/"

    def __get_audio_url_by_id(self, cart_id: str) -> str:
        """
            Gets the URL for a cart's audio based on its ID.

        Args:
            cart_id (str): The ID for the cart.

        Returns:
            str: The URL.
        """
        if self._secure:
            return f"https://{self._base_url}/api/audio/{cart_id}/"
        return f"http://{self._base_url}/api/audio/{cart_id}/"

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
        data = self.cart_to_dictionary(cart)
        response = post(self.__post_cart_url(), data, headers=headers)

        if response.ok:
            self._logger.info(
                f"Successfully added cart {cart.label} to the repository."
            )
        else:
            self._logger.error(
                f"Error code {response.status_code} adding cart {cart.label} to the repository."
            )
        return bool(response.ok)

    async def update(self, differences: Dict, cart_id: Cart) -> bool:
        self._logger.info(f"Attempting to update cart {cart_id} in the repository.")
        self._logger.debug(f"Updating cart {cart_id} with the following: {differences}")
        headers = await self._authenticator.generate_headers()
        response = patch(
            self.__get_cart_url_by_id(cart_id),
            differences,
            headers=headers,
        )

        if response.ok:
            self._logger.info(f"Successfully updated cart {cart_id} in the repository.")
        else:
            self._logger.error(
                f"Error code {response.status_code} updating cart {cart_id} in the repository."
            )
        return bool(response.ok)

    async def upload_audio(self, cart_id: str, file_path: Path) -> bool:
        self._logger.info(
            f"Attempting to upload audio for cart {cart_id} from {file_path}."
        )
        headers = await self._authenticator.generate_headers()
        files = {"file": file_path.open("rb")}
        response = post(
            self.__get_audio_url_by_id(cart_id), files=files, headers=headers
        )

        if response.ok:
            self._logger.info(
                f"Successfully uploaded audio for cart {cart_id} from {file_path}."
            )
        else:
            self._logger.error(
                f"Error code {response.status_code} uploading audio for cart {cart_id} from {file_path}."
            )
        return bool(response.ok)
