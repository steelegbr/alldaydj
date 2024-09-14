"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2022 Marc Steele
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

from alldaydj.models.user import User, Token
from alldaydj.services.cryptography import decode_token
from alldaydj.services.logging import logger
from alldaydj.services.user_repository import UserRepository
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

HEADER_BEARER = {"WWW-Authenticate": "Bearer"}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_repository = UserRepository()


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    creds_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers=HEADER_BEARER,
    )

    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if not email:
            raise creds_exception
        token = Token(email=email)
    except JWTError as ex:
        logger.warning(f"JWT token error: {ex}")
        raise creds_exception

    if user := user_repository.get(email):
        return user

    raise creds_exception
