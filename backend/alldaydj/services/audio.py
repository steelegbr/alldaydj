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

from enum import Enum
from io import BytesIO
from wave_chunk_parser.chunks import FormatChunk, RiffChunk, WaveFormat


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
