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

from datetime import datetime, timedelta
from jose import jwt
from os import environ
from passlib.context import CryptContext
from typing import Dict

SECRET_KEY_FILE = environ.get("ALLDAYDJ_SECRET_KEY_FILE")
TOKEN_EXPIRY_MINUTES = environ.get("ALLDAYDJ_TOKEN_EXPIRY", 30)
TOKEN_ALGORITHM = "ES512"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

with open(SECRET_KEY_FILE, "r") as secret_file:
    SECRET_KEY = secret_file.read()


def verify_password(plain: str, hashed: str) -> bool:
    return password_context.verify(plain, hashed)


def generate_password_hash(plain: str) -> str:
    return password_context.hash(plain)


def generate_access_token(email: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)

    return jwt.encode(
        {"exp": expire, "sub": email}, SECRET_KEY, algorithm=TOKEN_ALGORITHM
    )


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, TOKEN_ALGORITHM)
