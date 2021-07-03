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

from abc import ABC, abstractmethod
import ffmpeg
from logging import getLogger, Logger
import os
from tempfile import NamedTemporaryFile
from typing import BinaryIO, Dict, Literal


class AudioDecoder(ABC):
    """
    Generic audio decoder.
    """

    @abstractmethod
    def decode(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        pass


class OggEncoder:
    """
    OGG Vorbis Encoder.
    """

    __logger: Logger

    def __init__(self):
        self.__logger = getLogger(__name__)

    def encode(
        self, input_stream: BinaryIO, output_stream: BinaryIO, quality: int
    ) -> None:
        """
        Encodes wave audio to OGG vorbis.

        Args:
            input_stream (BinaryIO): The input file.
            output_stream (BinaryIO): The output file.
            quality (int): The quality to encode at.
        """

        with NamedTemporaryFile(
            suffix=".wav"
        ) as temp_in_file, NamedTemporaryFile() as temp_out_file:

            # Write our inbound (compressed) file to a temporary destination

            input_stream.seek(0)
            temp_in_file.write(input_stream.read())
            temp_in_file.flush()

            # Convert

            out_ogg_filename = f"{temp_out_file.name}.ogg"

            ffmpeg_stderr, ffmpeg_stdout = (
                ffmpeg.input(temp_in_file.name)
                .output(out_ogg_filename, q=quality)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )

            # Log the result

            self.__logger.info(
                "FFMPEG compression to OGG STDOUT: %s",
                ffmpeg_stdout,
            )
            self.__logger.info(
                "FFMPEG compression to OGG STDERR: %s",
                ffmpeg_stderr,
            )

            # Write to our buffer

            with open(out_ogg_filename, "rb") as converted_ogg:
                output_stream.write(converted_ogg.read())

            # Delete our WAV file

            os.remove(out_ogg_filename)


class MpegCodec(AudioDecoder):
    """
    Uses the FFMPEG library to encode and decode.
    """

    __file_format: Literal["ogg", "flac", "mp3"]
    __logger: Logger

    def __init__(self, file_format: Literal["ogg", "flac", "mp3"]):
        self.__file_format = file_format
        self.__logger = getLogger(__name__)

    def decode(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:

        with NamedTemporaryFile(
            suffix=f".{self.__file_format}"
        ) as temp_in_file, NamedTemporaryFile() as temp_out_file:

            # Write our inbound (compressed) file to a temporary destination

            input_stream.seek(0)
            temp_in_file.write(input_stream.read())
            temp_in_file.flush()

            # Convert

            out_wave_filename = f"{temp_out_file.name}.wav"

            ffmpeg_stderr, ffmpeg_stdout = (
                ffmpeg.input(temp_in_file.name)
                .output(out_wave_filename)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )

            # Log the result

            self.__logger.info(
                "FFMPEG conversion of %s STDOUT: %s",
                self.__file_format,
                ffmpeg_stdout,
            )
            self.__logger.info(
                "FFMPEG conversion of %s STDERR: %s",
                self.__file_format,
                ffmpeg_stderr,
            )

            # Write to our buffer

            with open(out_wave_filename, "rb") as converted_wav:
                output_stream.write(converted_wav.read())

            # Delete our WAV file

            os.remove(out_wave_filename)


def get_decoder(mime: str) -> AudioDecoder:
    """
    Returns the decoder for a given file mime type.

    Args:
        mime (str): The file mime type.

    Returns:
        AudioDecoder: The audio decoder to use.
    """

    if "ID3" in mime:
        return MpegCodec("mp3")
    if "Ogg data, Vorbis audio" in mime:
        return MpegCodec("ogg")
    if "FLAC" in mime:
        return MpegCodec("flac")
    if "AAC" in mime:
        return MpegCodec("m4a")

    raise ValueError(f"{mime} is not a supported compressed audio format.")
