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

from alldaydj.services.database import db, strip_id
from alldaydj.services.logging import logger
from pydantic import BaseModel
from typing import Callable
from uuid import UUID


class Repository:
    def get_document(self, id: UUID, collection: str, mapper: Callable):
        doc = db.collection(collection).document(str(id)).get()
        if doc.exists:
            logger.info(f"Document id {id} in {collection} exists")
            return mapper(doc)
        logger.info(f"Document id {id} in {collection} does not exist")

    def get_all(self, collection: str, mapper: Callable):
        [mapper(doc) for doc in db.collection(collection).stream()]

    def save_stripped_document(
        self, id: UUID, collection: str, doc: BaseModel, extra_fields={}
    ):
        converted = {**doc.dict(), **extra_fields}
        strip_id(converted)
        db.collection(collection).document(str(id)).set(converted)
