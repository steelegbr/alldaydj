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
from alldaydj.services.artist_repository import ArtistRepository
from alldaydj.services.repository import Repository
from alldaydj.services.database import db, strip_id
from alldaydj.services.logging import logger
from alldaydj.services.search import fields_to_tokens, fields_to_weighting_map
from typing import Dict, List
from uuid import UUID

COLLECTION_CART = "cart"
FIELD_SEARCH = "search"

artist_repository = ArtistRepository()


class CartRepository(Repository):
    def __map_doc_to_cart(self, cart_doc) -> Cart:
        return Cart.parse_obj({**cart_doc.to_dict(), "id": cart_doc.id})

    def __generate_search_field(self, cart: Cart) -> Dict[str, int]:
        return fields_to_weighting_map([cart.title, cart.artist])

    def get(self, id: UUID) -> Cart:
        logger.info(f"Lookup for cart ID {id}")
        return self.get_document(id, COLLECTION_CART, self.__map_doc_to_cart)

    def get_by_label(self, label: str) -> List[Cart]:
        logger.info(f"Lookup for cart by label {label}")
        return [
            self.__map_doc_to_cart(cart_doc)
            for cart_doc in db.collection(COLLECTION_CART)
            .where("label", "==", label)
            .stream()
        ]

    def get_by_label_prefix(self, prefix: str) -> List[Cart]:
        logger.info(f"Lookup for cart by label prefix {prefix}")
        return [
            self.__map_doc_to_cart(cart_doc)
            for cart_doc in db.collection(COLLECTION_CART)
            .where("label", ">=", prefix)
            .where("label", "<", f"{prefix}\uF8FF")
            .stream()
        ]

    def get_by_artist(self, artist: str) -> Cart:
        logger.info(f"Lookup for cart by artist {artist}")
        return [
            self.__map_doc_to_cart(cart_doc)
            for cart_doc in db.collection(COLLECTION_CART)
            .where("artist", "==", artist)
            .stream()
        ]

    def save(self, id: UUID, cart: Cart):
        logger.info(f"Saving cart ID {id}")
        self.save_stripped_document(
            id,
            COLLECTION_CART,
            cart,
            {FIELD_SEARCH: self.__generate_search_field(cart)},
        )

    def search(self, q: str) -> List[Cart]:
        logger.info(f"Search carts: {q}")

        search_tokens = fields_to_tokens([q])
        search_query = db.collection(COLLECTION_CART)

        for search_token in search_tokens:
            search_query = search_query.where(f"{FIELD_SEARCH}.{search_token}", "==", 1)

        return [self.__map_doc_to_cart(cart_doc) for cart_doc in search_query.stream()]

    def delete(self, id: UUID):
        logger.info(f"Delete cart ID {id}")
        db.collection(COLLECTION_CART).document(str(id)).delete()

    def delete_artist_if_not_used(self, cart: Cart):
        logger.info(f"Clean up for artist name {cart.artist}")
        if not self.get_by_artist(cart.artist):
            artist_to_delete = artist_repository.get_by_name(cart.artist)

            if not artist_to_delete:
                logger.warning(f"Failed to find artist {cart.artist} for cleanup")
            else:
                artist_repository.delete(artist_to_delete)
