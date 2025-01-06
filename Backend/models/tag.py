from models.mongo import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional


class Tag(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    tag: str


class TagUpdate(BaseModel):
    tag: str
