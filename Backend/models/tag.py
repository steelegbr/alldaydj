from pydantic import BaseModel, Field
from typing import Optional


class Tag(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    tag: str


class TagUpdate(BaseModel):
    tag: str
