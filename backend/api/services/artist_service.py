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

from database import db
from models.artist import Artist
from services.logging import logger
from typing import Optional
from uuid import UUID

COLLECTION_ARTIST = "artists"


class ArtistService:
    def get(self, id: UUID) -> Optional[Artist]:
        logger.info(f"Lookup for artist ID {id}")
        artist_ref = db.collection(COLLECTION_ARTIST).document(id)
        artist_doc = artist_ref.doc()
        if artist_doc.exists():
            logger.info(f"Artist ID {id} found")
            return artist_doc.to_dict()
        logger.info(f"Artist id {id} NOT found")
