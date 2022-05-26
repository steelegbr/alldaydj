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

from alldaydj.services.logging import logger
from enum import Enum
from io import BytesIO
from typing import List, Tuple
from wave_chunk_parser.chunks import CartChunk, FormatChunk, RiffChunk, WaveFormat


class WaveCompression(Enum):
    UNCOMPRESSED = 0
    COMPRESSED = 1
    INVALID = 2


def get_wave_compression(blob: bytes) -> WaveCompression:
    try:
        file = BytesIO(blob)
        riff_chunk = RiffChunk.from_file(file)
        format_chunk: FormatChunk = riff_chunk.sub_chunks.get(FormatChunk.HEADER_FORMAT)
        if format_chunk and format_chunk.format == WaveFormat.PCM:
            return WaveCompression.UNCOMPRESSED
        return WaveCompression.COMPRESSED
    except Exception:
        return WaveCompression.INVALID


def get_cart_chunk(blob: bytes) -> Tuple[CartChunk, FormatChunk]:
    try:
        riff_chunk = RiffChunk.from_file(blob)
        return (
            riff_chunk.sub_chunks.get(CartChunk.HEADER_CART),
            riff_chunk.sub_chunks.get(FormatChunk.HEADER_FORMAT),
        )
    except Exception as ex:
        logger.warning(f"Failed to read chunks from file. Reason: {ex}")
        return (None, None)


def timer_to_milliseconds(
    cart_chunk: CartChunk, format_chunk: FormatChunk, possible_prefixes: List[str]
) -> int:
    for prefix in possible_prefixes:
        if found_timers := [
            timer for timer in cart_chunk.timers if timer.name == prefix
        ]:
            return (found_timers[0].time * 1000) // format_chunk.sample_rate
    return 0
