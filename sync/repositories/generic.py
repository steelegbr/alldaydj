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

from alldaydj.http import Authenticator
from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from urllib.parse import quote_plus, urlencode


class MsSqlRepository:
    """
    Base class for an MS SQL repository.
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


class AllDayDjRepository:
    """
    Base class for an AllDay DJ repository.
    """

    _authenticator: Authenticator
    _logger: Logger
    _base_url: str
    _secure: bool

    def __init__(
        self, authenticator: Authenticator, logger: Logger, base_url: str, secure: bool
    ):
        self._authenticator = authenticator
        self._logger = logger
        self._base_url = base_url
        self._secure = secure
