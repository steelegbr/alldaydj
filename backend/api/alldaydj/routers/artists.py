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
from alldaydj.services.artist_repository import ArtistRepository
from fastapi import APIRouter, HTTPException, Response
from fastapi_pagination import Page, add_pagination, paginate
from typing import List
from uuid import uuid4, UUID

router = APIRouter()
artist_repository = ArtistRepository()


@router.get("/artist/{artist_id}")
async def get_artist(artist_id: UUID) -> Artist:
    if not (artist := artist_repository.get(artist_id)):
        raise HTTPException(status_code=404, detail="Artist not found")

    return artist


@router.post("/artist/")
async def create_artist(artist: Artist) -> Artist:
    if artist_repository.get_by_name(artist.name):
        raise HTTPException(
            status_code=409, detail="Artist with that name already exists"
        )

    id = uuid4()
    artist_repository.save(id, artist)
    artist.id = id

    return artist


@router.delete("/artist/{artist_id}")
async def delete_artist(artist_id: UUID):
    artist = artist_repository.get(artist_id)

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    artist_repository.delete(artist_id)
    return Response(status_code=204)


@router.get("/artist/", response_model=Page[Artist])
async def autocomplete_artist(q: str) -> List[Artist]:
    return paginate(artist_repository.autocomplete_search(q))


add_pagination(router)
