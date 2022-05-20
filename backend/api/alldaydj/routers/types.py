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

from alldaydj.models.cart import CartType
from alldaydj.services.type_respository import TypeRepository
from fastapi import APIRouter, HTTPException, Response
from fastapi_pagination import Page, add_pagination, paginate
from typing import List
from uuid import UUID, uuid4

router = APIRouter()
type_repository = TypeRepository()


@router.get("/type", response_model=Page[CartType])
async def get_types() -> List[CartType]:
    return paginate(type_repository.all())


@router.post("/type")
async def create_type(cart_type: CartType) -> CartType:
    if type_repository.get_by_tag(cart_type.tag):
        raise HTTPException(
            status_code=409, detail="Cart type with that tag already exists"
        )

    id = uuid4()
    type_repository.save(id, cart_type)
    cart_type.id = id

    return cart_type


@router.put("/type/{type_id}")
async def update_type(type_id: UUID, cart_type: CartType) -> CartType:
    if not type_repository.get(type_id):
        raise HTTPException(status_code=404, detail="Cart type not found")

    type_repository.save(type_id, cart_type)
    cart_type.id = type_id
    return cart_type


@router.delete("/type/{type_id}")
async def delete_type(type_id: UUID):
    if not type_repository.get(type_id):
        raise HTTPException(status_code=404, detail="Cart type not found")

    type_repository.delete(type_id)
    return Response(status_code=204)


add_pagination(router)
