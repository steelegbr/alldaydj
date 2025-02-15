from datetime import datetime
from models.dto.base import ApiBaseModel
from typing import List, Optional


class CartType(ApiBaseModel):
    cart_type: str


class Genre(ApiBaseModel):
    genre: str


class Tag(ApiBaseModel):
    tag: str


class Cart(ApiBaseModel):
    id: Optional[str]
    label: str
    artist: str
    title: str
    album: str
    type: CartType
    genre: Genre
    year: int
    tags: List[Tag]
    sweeper: bool
    override_fade: bool
    valid_from: datetime
    valid_to: datetime
    isrc: str
    record_label: str
