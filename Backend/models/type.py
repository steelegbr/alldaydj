from models.mongodb import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional


class CartType(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    cart_type: str


class CartTypeUpdate(BaseModel):
    cart_type: str
