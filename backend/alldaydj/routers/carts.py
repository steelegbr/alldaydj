"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2022 Marc Steele
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from alldaydj.models.cart import Cart
from alldaydj.services.artist_repository import ArtistRepository
from alldaydj.services.cart_repository import CartRepository
from alldaydj.services.type_respository import TypeRepository
from alldaydj.services.logging import logger
from fastapi import APIRouter, HTTPException, Response
from fastapi_pagination import Page, add_pagination, paginate
from typing import List
from uuid import UUID, uuid4

router = APIRouter()
artist_repository = ArtistRepository()
cart_repository = CartRepository()
type_repository = TypeRepository()


@router.get("/cart/{cart_id}")
async def get_cart(cart_id: UUID) -> Cart:
    cart = cart_repository.get(cart_id)

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart


@router.get("/cart/by-label/{label}")
async def get_cart_by_label(label: str) -> Cart:
    carts = cart_repository.get_by_label(label)

    if not carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    if len(carts) > 1:
        cart_ids = [cart.id for cart in carts]
        logger.error(f"Found multiple carts for label {label}: {cart_ids}")
        raise HTTPException(
            status_code=500, detail="Multiple carts found for the supplied label"
        )

    return carts[0]


@router.post("/cart")
async def create_cart(cart: Cart) -> Cart:
    if cart_repository.get_by_label(cart.label):
        raise HTTPException(
            status_code=409, detail="Cart with that label already exists"
        )

    # Re-map the type to a UUID

    cart.type = type_repository.remap_string_to_uuid(cart.type)

    # Perform the save

    id = uuid4()
    cart_repository.save(id, cart)
    cart.id = id

    # Add the artist as needed

    artist_repository.add_if_not_exist(cart.artist)
    return cart


@router.get("/cart", response_model=Page[Cart])
async def search_cart(q: str) -> List[Cart]:
    return paginate(cart_repository.search(q))


@router.put("/cart/{cart_id}")
async def update_cart(cart_id: UUID, cart: Cart) -> Cart:
    if not (existing_cart := cart_repository.get(cart_id)):
        raise HTTPException(status_code=404, detail="Cart not found")

    # Re-map the type to a UUID

    cart.type = type_repository.remap_string_to_uuid(cart.type)

    # Save the cart and do any artist mapping magic

    cart_repository.save(cart_id, cart)
    cart_repository.delete_artist_if_not_used(existing_cart)
    artist_repository.add_if_not_exist(cart.artist)

    cart.id = cart_id
    return cart


@router.delete("/cart/{cart_id}")
async def delete_cart(cart_id):
    if not (existing_cart := cart_repository.get(cart_id)):
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_repository.delete(cart_id)
    cart_repository.delete_artist_if_not_used(existing_cart)

    return Response(status_code=204)


add_pagination(router)
