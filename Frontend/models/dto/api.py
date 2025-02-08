from pydantic import BaseModel
from typing import Generic, List, TypeVar

T = TypeVar("T")


class ApiSettings(BaseModel):
    auth_audience: str
    auth_domain: str
    auth_client_id: str


class Pagination(BaseModel, Generic[T]):
    items: List[T]
    page: int
    pages: int
    size: int
    total: int
