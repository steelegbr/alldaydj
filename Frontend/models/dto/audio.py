from models.dto.base import ApiBaseModel


class CartType(ApiBaseModel):
    cart_type: str


class Genre(ApiBaseModel):
    genre: str


class Tag(ApiBaseModel):
    tag: str
