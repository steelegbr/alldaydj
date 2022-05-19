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

from fastapi import APIRouter, HTTPException
from models.artist import Artist
from services.artist_service import ArtistService
from services.logging import logger
from uuid import UUID

router = APIRouter()
artist_service = ArtistService()


@router.get("/{artist_id}")
def get_artist(artist_id: UUID) -> Artist:
    logger.info(f"GET for artist ID {artist_id}")
    artist = artist_service.get(artist_id)

    if not artist:
        logger.info(f"RETURN 404 artist ID {artist_id}")
        raise HTTPException(status_code=404, detail="Artist not found")

    logger.info(f"RETURN 200 artist ID {artist_id}")
    return artist
