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
from fastapi import APIRouter, HTTPException, Response
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import constr
from typing import List

router = APIRouter()
artist_repository = ArtistRepository()
cart_repository = CartRepository()
type_repository = TypeRepository()


@router.get("/cart/{label}")
async def get_cart(label: str = constr(regex=r"[a-zA-Z0-9]+")) -> Cart:
    cart = cart_repository.get(label)

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart


@router.post("/cart")
async def create_cart(cart: Cart) -> Cart:
    if cart_repository.get(cart.label):
        raise HTTPException(
            status_code=409, detail="Cart with that label already exists"
        )

    # Re-map the type to a UUID

    cart.type = type_repository.remap_string_to_uuid(cart.type)

    # Perform the save

    cart_repository.save(cart)

    # Add the artist as needed

    artist_repository.add_if_not_exist(cart.artist)
    return cart


@router.get("/cart", response_model=Page[Cart])
async def search_cart(q: str) -> List[Cart]:
    return paginate(cart_repository.search(q))


@router.put("/cart/{label}")
async def update_cart(label: str, cart: Cart) -> Cart:
    if not (existing_cart := cart_repository.get(label)):
        raise HTTPException(status_code=404, detail="Cart not found")

    # Re-map the type to a UUID

    cart.type = type_repository.remap_string_to_uuid(cart.type)

    # Save the cart and do any artist mapping magic

    cart_repository.save(cart)
    cart_repository.delete_artist_if_not_used(existing_cart)
    artist_repository.add_if_not_exist(cart.artist)

    return cart


@router.delete("/cart/{label}")
async def delete_cart(label):
    if not (existing_cart := cart_repository.get(label)):
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_repository.delete(label)
    cart_repository.delete_artist_if_not_used(existing_cart)

    return Response(status_code=204)


add_pagination(router)
