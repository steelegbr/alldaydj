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

import re

from sys import prefix
from alldaydj.models.cart import Cart
from alldaydj.models.sequencer import CartIdSequencer
from alldaydj.services.cart_repository import CartRepository
from alldaydj.services.sequencer_repository import SequencerRepository
from fastapi import APIRouter, HTTPException, Response
from fastapi_pagination import Page, add_pagination, paginate
from typing import List
from uuid import UUID, uuid4

from backend.api.alldaydj.models.sequencer import SequencerResponse

router = APIRouter()
cart_repository = CartRepository()
seq_repository = SequencerRepository()


@router.get("/sequencer", response_model=Page[CartIdSequencer])
async def get_sequencers() -> List[CartIdSequencer]:
    return paginate(seq_repository.all())


@router.get("/sequencer/{sequencer_id}")
async def get_sequencer(sequencer_id: UUID) -> CartIdSequencer:
    return seq_repository.get(sequencer_id)


@router.post("/sequencer/")
async def create_sequencer(sequencer: CartIdSequencer) -> CartIdSequencer:
    if seq_repository.get_by_name(sequencer.name):
        raise HTTPException(
            status_code=409, detail="Sequencer with that name already exists"
        )

    id = uuid4()
    seq_repository.save(id, sequencer)
    sequencer.id = id

    return sequencer


@router.put("/sequencer/{sequencer_id}")
async def update_sequencer(
    sequencer_id: UUID, sequencer: CartIdSequencer
) -> CartIdSequencer:
    if not seq_repository.get(sequencer_id):
        raise HTTPException(status_code=404, detail="Sequencer not found")

    seq_repository.save(sequencer_id, sequencer)
    sequencer.id = sequencer_id
    return sequencer


@router.delete("/sequencer/{sequencer_id}")
async def delete_sequencer(sequencer_id: UUID):
    if not seq_repository.get(sequencer_id):
        raise HTTPException(status_code=404, detail="Sequencer not found")

    seq_repository.delete(sequencer_id)
    return Response(status_code=204)


@router.get("/sequencer/{sequencer_id}/generate_next")
async def generate_next_cart_id(sequencer_id: UUID) -> SequencerResponse:
    if not (sequencer := seq_repository.get(sequencer_id)):
        raise HTTPException(status_code=404, detail="Sequencer not found")

    labels_with_prefix = sorted(
        [cart.label for cart in cart_repository.get_by_label_prefix(sequencer.prefix)]
    )

    label_regex = (
        f"{sequencer.prefix}(\\d{{{sequencer.min_digits},}}){sequencer.suffix}"
    )

    existing_cart_numbers = [
        int(match.group(1))
        for label in labels_with_prefix
        if (match := re.match(label_regex, label))
    ]

    next_free = next(
        i for i, e in enumerate(existing_cart_numbers + [None], 1) if i != e
    )
    next_padded = str(next_free).rjust(sequencer.min_digits, "0")
    next_cart_label = f"{sequencer.prefix}{next_padded}{sequencer.suffix}"

    return SequencerResponse(next=next_cart_label)


add_pagination(router)
