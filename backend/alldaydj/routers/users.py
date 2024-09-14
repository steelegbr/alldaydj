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
from alldaydj.services.cryptography import generate_access_token
from alldaydj.services.user_repository import UserRepository
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

HEADER_BEARER = {"WWW-Authenticate": "Bearer"}

router = APIRouter()
user_repository = UserRepository()


@router.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> Token:
    if not user_repository.authenticate(form.username, form.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username and/or password",
            headers=HEADER_BEARER,
        )

    return Token(access_token=generate_access_token(form.username))
