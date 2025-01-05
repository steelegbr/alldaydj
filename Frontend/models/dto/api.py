from pydantic import BaseModel, HttpUrl
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class ApiSettings(BaseModel):
    auth_audience: str
    auth_domain: str
    auth_client_id: str


class Pagination(BaseModel, Generic[T]):
    count: int
    next: Optional[HttpUrl]
    previous: Optional[HttpUrl]
    results: List[T]
