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

from alldaydj.models import AudioUploadJob
from enum import Enum
from typing import BinaryIO, Tuple
from wave_chunk_parser.chunks import RiffChunk, FormatChunk, CartChunk, WaveFormat


class WaveCompression(Enum):
    UNCOMPRESSED = 0
    COMPRESSED = 1
    INVALID = 2


def get_wave_compression(file: BinaryIO) -> WaveCompression:
    """
    Indicates the level of compression on a wave file.

    Args:
        file (BinaryIO): The file handle.

    Returns:
        WaveCompression: The level of compression detected.
    """

    try:

        riff_chunk = RiffChunk.from_file(file)
        format_chunk: FormatChunk = riff_chunk.sub_chunks.get(FormatChunk.HEADER_FORMAT)
        if format_chunk and format_chunk.format == WaveFormat.PCM:
            return WaveCompression.UNCOMPRESSED
        return WaveCompression.COMPRESSED

    # skipcq: PYL-W0703
    # Any issues reading the file means it's not valid.
    except Exception:

        # If we get here we didn't see a format chunk

        return WaveCompression.INVALID


def get_cart_chunk(file: BinaryIO) -> Tuple[CartChunk, FormatChunk]:
    """
    Attempts to get a cart chunk from a WAVE file.

    Args:
        file (BinaryIO): The file to find the chunk in.

    Returns:
        Tuple[CartChunk, FormatChunk]: The chunk if we can find it and an associated format chunk.
    """

    try:
        riff_chunk = RiffChunk.from_file(file)
        return (
            riff_chunk.sub_chunks.get(CartChunk.HEADER_CART),
            riff_chunk.sub_chunks.get(FormatChunk.HEADER_FORMAT),
        )
    # skipcq: PYL-W0703
    # Fall back to assuming there's not metadata.
    except Exception:
        return (None, None)


class FileStage(Enum):
    """
    The possible stages an audio file can be in.
    """

    QUEUED = 0
    COMPRESSED = 1
    AUDIO = 2


def generate_file_name(job: AudioUploadJob, stage: FileStage) -> str:
    """
    Generates the name of an audio file based on the stage.

    Args:
        job_id (AudioUploadJob): The job we're doing this for.
        stage (FileStage): The stage the file is in.

    Returns:
        str: The file name.
    """

    if stage == FileStage.QUEUED:
        return f"queued/{job.id}_{job.cart.id}"
    if stage == FileStage.COMPRESSED:
        return f"compressed/{job.cart.id}"

    return f"audio/{job.cart.id}"
