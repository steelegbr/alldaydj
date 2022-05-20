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

from alldaydj.models.artist import Artist
from alldaydj.services.database import db, strip_id
from alldaydj.services.logging import logger
from typing import List, Optional
from uuid import UUID

COLLECTION_ARTIST = "artists"
FIELD_AUTOCOMPLTE = "autocomplete"


class ArtistRepository:
    def __map_doc_to_artist(self, artist_doc) -> Artist:
        return Artist.parse_obj({**artist_doc.to_dict(), "id": artist_doc.id})

    def get(self, id: UUID) -> Optional[Artist]:
        logger.info(f"Lookup for artist ID {id}")
        artist_doc = db.collection(COLLECTION_ARTIST).document(str(id)).get()
        if artist_doc.exists:
            logger.info(f"Artist ID {id} found")
            return self.__map_doc_to_artist(artist_doc)
        logger.info(f"Artist ID {id} NOT found")

    def get_by_name(self, name: str) -> List[Artist]:
        logger.info(f"Find exact match of artist name {name}")
        return [
            self.__map_doc_to_artist(artist_doc)
            for artist_doc in db.collection(COLLECTION_ARTIST)
            .where("name", "==", name)
            .stream()
        ]

    def save(self, id: str, artist: Artist):
        logger.info(f"Saving artist {id}")

        # Convert

        artist_to_save = artist.dict()
        strip_id(artist_to_save)

        # Create an autocomplete field

        artist_to_save[FIELD_AUTOCOMPLTE] = artist.name.lower()

        # Save

        db.collection(COLLECTION_ARTIST).document(str(id)).set(artist_to_save)

    def delete(self, id: UUID):
        logger.info(f"Delete artist {id}")
        db.collection(COLLECTION_ARTIST).document(str(id)).delete()

    def autocomplete_search(self, q: str) -> List[Artist]:
        logger.info(f"Search artist name {q}")
        return [
            self.__map_doc_to_artist(artist_doc)
            for artist_doc in db.collection(COLLECTION_ARTIST)
            .where(FIELD_AUTOCOMPLTE, ">=", q)
            .where(FIELD_AUTOCOMPLTE, "<", f"q\uF8FF")
            .stream()
        ]
