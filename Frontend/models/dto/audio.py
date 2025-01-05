from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Tag(BaseModel):
    id: Optional[UUID]
    tag: str
