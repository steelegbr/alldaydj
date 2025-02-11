from pydantic import BaseModel
from typing import Optional


class ApiBaseModel(BaseModel):
    id: Optional[str]
