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

from alldaydj.models.cart import Cart
from alldaydj.services.database import db, strip_id
from alldaydj.services.logging import logger
from alldaydj.services.search import fields_to_tokens, fields_to_weighting_map
from typing import Dict, List
from uuid import UUID

COLLECTION_CART = "cart"
FIELD_SEARCH = "search"


class CartRepository:
    def __map_doc_to_cart(self, cart_doc) -> Cart:
        return Cart.parse_obj({**cart_doc.to_dict(), "id": cart_doc.id})

    def __generate_search_field(self, cart_dict) -> Dict[str, int]:
        return fields_to_weighting_map([cart_dict["title"], cart_dict["artist"]])

    def get(self, id: UUID) -> Cart:
        logger.info(f"Lookup for cart ID {id}")
        cart_doc = db.collection(COLLECTION_CART).document(str(id)).get()
        if cart_doc.exists:
            logger.info(f"Cart ID {id} found")
            return self.__map_doc_to_cart(cart_doc)
        logger.info(f"Cart ID {id} NOT found")

    def get_by_label(self, label: str) -> Cart:
        logger.info(f"Lookup for cart by label {label}")
        return [
            self.__map_doc_to_cart(cart_doc)
            for cart_doc in db.collection(COLLECTION_CART)
            .where("label", "==", label)
            .stream()
        ]

    def save(self, id: UUID, cart: Cart):
        logger.info(f"Saving cart ID {id}")

        # Convert

        cart_to_save = cart.dict()
        strip_id(cart_to_save)
        cart_to_save[FIELD_SEARCH] = self.__generate_search_field(cart_to_save)

        # Save

        db.collection(COLLECTION_CART).document(str(id)).set(cart_to_save)

    def search(self, q: str) -> List[Cart]:
        logger.info(f"Search carts: {q}")

        search_tokens = fields_to_tokens([q])
        search_query = db.collection(COLLECTION_CART)

        for search_token in search_tokens:
            search_query = search_query.where(f"{FIELD_SEARCH}.{search_token}", "==", 1)

        return [self.__map_doc_to_cart(cart_doc) for cart_doc in search_query.stream()]
