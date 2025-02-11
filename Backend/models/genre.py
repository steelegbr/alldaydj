from models.mongodb import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional


class Genre(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    genre: str


class GenreUpdate(BaseModel):
    genre: str
