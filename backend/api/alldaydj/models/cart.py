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

from turtle import st
from typing import Optional, List
from pydantic import BaseModel, constr, Field
from pydantic.color import Color
from uuid import UUID


class Cart(BaseModel):
    id: Optional[UUID]
    label: constr(regex=r"[a-zA-Z0-9]+")
    title: str
    artist: str
    cue_audio_start: int = Field(default=0, ge=0)
    cue_audio_end: int = Field(default=0, ge=0)
    cue_intro_end: int = Field(default=0, ge=0)
    cue_segue: int = Field(default=0, ge=0)
    sweeper: bool
    year: int = Field(default=0, ge=0)
    isrc: Optional[str]
    composer: Optional[str]
    publisher: Optional[str]
    record_label: Optional[str]
    tags: List[str]
    type: str
    hash_audio: Optional[str]
    hash_compressed: Optional[str]
    audio: Optional[str]
    compressed: Optional[str]
    fade: bool


class CartType(BaseModel):
    id: Optional[UUID]
    tag: constr(min_length=1)
    colour: Color
    now_playing: bool
