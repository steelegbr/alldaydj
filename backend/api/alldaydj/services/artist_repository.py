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
from alldaydj.services.repository import Repository
from typing import List, Optional
from uuid import UUID, uuid4

COLLECTION_ARTIST = "artists"
FIELD_AUTOCOMPLTE = "autocomplete"


class ArtistRepository(Repository):
    def __map_doc_to_artist(self, artist_doc) -> Artist:
        return Artist.parse_obj({**artist_doc.to_dict(), "id": artist_doc.id})

    def get(self, id: UUID) -> Optional[Artist]:
        logger.info(f"Lookup for artist ID {id}")
        return self.get_document(id, COLLECTION_ARTIST, self.__map_doc_to_artist)

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
        self.save_stripped_document(
            id, COLLECTION_ARTIST, artist, {FIELD_AUTOCOMPLTE: artist.name.lower()}
        )

    def delete(self, id: UUID):
        logger.info(f"Delete artist {id}")
        db.collection(COLLECTION_ARTIST).document(str(id)).delete()

    def autocomplete_search(self, q: str) -> List[Artist]:
        logger.info(f"Search artist name {q}")
        return [
            self.__map_doc_to_artist(artist_doc)
            for artist_doc in db.collection(COLLECTION_ARTIST)
            .where(FIELD_AUTOCOMPLTE, ">=", q)
            .where(FIELD_AUTOCOMPLTE, "<", f"{q}\uF8FF")
            .stream()
        ]

    def add_if_not_exist(self, name: str):
        logger.info(f"Add artist name {name} if they do not already exist")
        if self.get_by_name(name):
            logger.info(f"Artist name {name} already exists")

        new_artist = Artist()
        new_artist.id = uuid4
        new_artist.name = name

        self.save(new_artist)
