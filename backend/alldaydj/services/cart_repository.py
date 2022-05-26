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
from hashlib import sha256
from typing import Dict, List
from uuid import UUID

COLLECTION_CART = "cart"
FIELD_SEARCH = "search"
FIELD_LABEL = "label"

artist_repository = ArtistRepository()


class CartRepository(Repository):
    def __map_doc_to_cart(self, cart_doc) -> Cart:
        return Cart.parse_obj({**cart_doc.to_dict(), "id": cart_doc.id})

    def __generate_search_field(self, cart: Cart) -> Dict[str, int]:
        return fields_to_weighting_map([cart.title, cart.artist])

    def normalise_label(self, label: str) -> str:
        return label.upper()

    def __label_to_id(self, label: str) -> str:
        encoded_label = self.normalise_label(label).encode("utf-8")
        return sha256(encoded_label).hexdigest()

    def generate_file_name(self, cart: Cart) -> str:
        return f"audio/{self.__label_to_id(cart.label)}"

    def get(self, label: str) -> Cart:
        logger.info(f"Lookup for cart label {label}")
        return self.get_document(
            self.__label_to_id(label), COLLECTION_CART, self.__map_doc_to_cart
        )

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

    def save(self, cart: Cart):
        logger.info(f"Saving cart label {cart.label}")
        self.save_stripped_document(
            self.__label_to_id(cart.label),
            COLLECTION_CART,
            cart,
            {
                FIELD_SEARCH: self.__generate_search_field(cart),
                FIELD_LABEL: cart.label.upper(),
            },
        )

    def search(self, q: str) -> List[Cart]:
        logger.info(f"Search carts: {q}")

        search_tokens = fields_to_tokens([q])
        search_query = db.collection(COLLECTION_CART)

        for search_token in search_tokens:
            search_query = search_query.where(f"{FIELD_SEARCH}.{search_token}", "==", 1)

        return [self.__map_doc_to_cart(cart_doc) for cart_doc in search_query.stream()]

    def delete(self, label: str):
        logger.info(f"Delete cart label {label}")
        db.collection(COLLECTION_CART).document(self.__label_to_id(label)).delete()

    def delete_artist_if_not_used(self, cart: Cart):
        logger.info(f"Clean up for artist name {cart.artist}")
        if not self.get_by_artist(cart.artist):
            artist_to_delete = artist_repository.get_by_name(cart.artist)

            if not artist_to_delete:
                logger.warning(f"Failed to find artist {cart.artist} for cleanup")
            else:
                artist_repository.delete(artist_to_delete)
