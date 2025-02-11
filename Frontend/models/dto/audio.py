from pydantic import BaseModel
from typing import Optional


class CartType(BaseModel):
    id: Optional[str]
    cart_type: str


class Genre(BaseModel):
    id: Optional[str]
    genre: str


class Tag(BaseModel):
    id: Optional[str]
    tag: str
