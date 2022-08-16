"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

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

import hashlib
from typing import BinaryIO


def generate_hash(byte_stream: BinaryIO) -> str:
    """
    Generates a SHA256 hash of a given byte stream.

    Args:
        byte_stream (BinaryIO): The stream to get the hash of.

    Returns:
        str: The SHA256 hash.
    """
    byte_stream.seek(0)
    hashed_stream = hashlib.sha256(byte_stream.read())
    return hashed_stream.hexdigest()