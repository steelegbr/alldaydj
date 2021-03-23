from abc import ABC, abstractmethod


class CartType:
    """
    Specifies a type of cart the system can know about.
    """

    _name: str
    _now_playing: bool

    def __init__(self, name: str, now_playing: bool):
        """
            Creates a new instance of a cart type.

        Args:
            name (str): The name of the cart type.
            now_playing (bool): Indicates if the type should appear in now playing.
        """
        self._name = name
        self._now_playing = now_playing

    @property
    def name(self) -> str:
        """
            Gets the name of the cart type.

        Returns:
            str: The name of the cart type.
        """
        return self._name

    @property
    def now_playing(self) -> bool:
        """
            Indicates if the type should appear in now playing.

        Returns:
            bool: TRUE if it should.
        """
        return self._now_playing


class TypeRepository(ABC):
    """
    Repository for holding cart types.
    """

    @abstractmethod
    def get_all(self) -> List[CartType]:
        pass


class PlayoutOneTypeRepository(TypeRepository):
    pass
