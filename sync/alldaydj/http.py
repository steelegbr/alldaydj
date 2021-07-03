"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from asyncio import Lock
from datetime import datetime, timezone
from jwt import decode
from logging import Logger
from requests import post


class Authenticator:
    """
    Provides utility methods for authenticating a user against AllDay DJ.
    """

    __instance__ = None
    __logger: Logger
    __secure: bool = False
    __url: str
    __username: str
    __password: str
    __lock: Lock
    __token_refresh: str
    __token_access: str
    __valid_token_refresh: datetime = None
    __valid_token_access: datetime = None

    def __init__(
        self,
        secure: bool,
        url: str,
        username: str,
        password: str,
        logger: Logger,
    ):
        if Authenticator.__instance__ is None:
            Authenticator.__instance__ = self
        else:
            raise Exception("Singleton can only be instantiated once.")

        self.__secure = secure
        self.__url = url
        self.__username = username
        self.__password = password
        self.__logger = logger
        self.__lock = Lock()

    @staticmethod
    def instance(secure: bool, url: str, username: str, password: str, logger: Logger):
        """
            Instantiates the authenticator.

        Args:
            secure (bool): Indicates if the connection should be secure.
            url (string): The URL to connect to.
            username (string): The username to log in with.
            password (string): The password to log in with.
            logger (Logger): Logger to record into.

        Returns:
            Authenticator: [description]
        """
        if not Authenticator.__instance__:
            Authenticator(secure, url, username, password, logger)
        return Authenticator.__instance__

    async def get_token(self) -> str:
        """
            Obtains a currently valid token to make API requests with.

        Returns:
            str: The token.
        """
        async with self.__lock:

            # Check if the current token is valid

            if self.__valid_token_access and self.__valid_token_access > datetime.now(
                timezone.utc
            ):
                self.__logger.info("Access token is still valid.")
                return self.__token_access

            # Fall back to the refresh token and get a new access token

            if (
                self.__valid_token_refresh
                and self.__valid_token_refresh > datetime.now(timezone.utc)
            ):
                self.__logger.info(
                    "Refresh token is still valid, obtaining new access token."
                )

            # Final fallback to using the username and password

            self.__logger.info("No valid tokens. New login session.")
            self.__get_refresh_token()
            return self.__token_access

    async def generate_headers(self):
        """
            Generates the headers to make an authenticated request.

        Returns:
            object: The headers to use in a HTTP request.
        """
        return {"Authorization": f"Bearer {await self.get_token()}"}

    def __get_url(self, path: str) -> str:
        """
        Obtains the URL to make requests against.
        """

        if self.__secure:
            return f"https://{self.__url}{path}"

        return f"http://{self.__url}{path}"

    def __get_refresh_token(self):
        """
        Obtains a new refresh token.
        """

        url = self.__get_url("/api/token/")
        self.__logger.info(f"Obtaining tokens from {url}")
        response = post(url, {"username": self.__username, "password": self.__password})
        response.raise_for_status()

        response_parts = response.json()
        self.__token_access = response_parts["access"]
        self.__token_refresh = response_parts["refresh"]
        self.__valid_token_access = self.__expiry_date_from_token(self.__token_access)
        self.__valid_token_refresh = self.__expiry_date_from_token(self.__token_refresh)

        self.__logger.info(f"Access token expires {self.__valid_token_access}")
        self.__logger.info(f"Refresh token expires {self.__valid_token_refresh}")

    @staticmethod
    def __expiry_date_from_token(token: str) -> datetime:
        """
            Calculates the exipry date for a token.

        Args:
            token (str): The token to decode.

        Returns:
            datetime: The exipry date.
        """
        claims = decode(token, options={"verify_signature": False})
        if claims and "exp" in claims:
            return datetime.fromtimestamp(claims["exp"], tz=timezone.utc)
