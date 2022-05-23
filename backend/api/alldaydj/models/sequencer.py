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

from pydantic import BaseModel, constr, Field
from typing import Optional
from uuid import UUID

CONSTRAINT_CART_ID = r"[a-zA-Z0-9]*"


class CartIdSequencer(BaseModel):
    id: Optional[UUID]
    name: constr(min_length=1)
    prefix: constr(regex=CONSTRAINT_CART_ID)
    suffix: constr(regex=CONSTRAINT_CART_ID)
    min_digits: Field(ge=1)


class SequencerResponse(BaseModel):
    next: str
