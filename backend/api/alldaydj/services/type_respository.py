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

from alldaydj.models.cart import CartType
from alldaydj.services.database import db, strip_id
from alldaydj.services.logging import logger
from typing import List
from uuid import UUID

COLLECTION_TYPE = "types"


class TypeRepository:
    def __map_doc_to_cart_type(self, type_doc) -> CartType:
        return CartType.parse_obj({**type_doc.to_dict(), "id": type_doc.id})

    def all(self) -> List[CartType]:
        logger.info("List for all cart types")
        return [
            self.__map_doc_to_cart_type(type_doc)
            for type_doc in db.collection(COLLECTION_TYPE).stream()
        ]

    def get(self, id: UUID) -> CartType:
        logger.info(f"Lookup for cart type ID {id}")
        type_doc = db.collection(COLLECTION_TYPE).document(str(id)).get()
        if type_doc.exists:
            logger.info(f"Cart type ID {id} found")
            return self.__map_doc_to_cart_type(type_doc)
        logger.info(f"Cart type ID {id} NOT found")

    def get_by_tag(self, tag: str) -> List[CartType]:
        logger.info(f"Lookup by cart type tag {tag}")
        return [
            self.__map_doc_to_cart_type(type_doc)
            for type_doc in db.collection(COLLECTION_TYPE)
            .where("tag", "==", tag)
            .stream()
        ]

    def save(self, id: UUID, cart_type: CartType):
        logger.info(f"Saving cart type {id}")

        # Convert

        cart_type_to_save = cart_type.dict()
        strip_id(cart_type_to_save)
        cart_type_to_save["colour"] = str(cart_type_to_save["colour"])

        # Save

        db.collection(COLLECTION_TYPE).document(str(id)).set(cart_type_to_save)

    def delete(self, id: UUID):
        logger.info(f"Deleting cart type {id}")
        db.collection(COLLECTION_TYPE).document(str(id)).delete()
