from abc import ABC, abstractmethod
import ffmpeg
from logging import getLogger, Logger
import numpy as np
import os
from streamp3 import MP3Decoder
from tempfile import NamedTemporaryFile
from typing import BinaryIO, Dict, Literal
from wave_chunk_parser.chunks import (
    RiffChunk,
    DataChunk,
    FormatChunk,
    WaveFormat,
    Chunk,
)


class AudioDecoder(ABC):
    """
    Generic audio decoder.
    """

    @abstractmethod
    def decode(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        pass


class Mp3AudioDecoder(AudioDecoder):
    """
    LAME based MP3 audio decoder.
    """

    def decode(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:

        # Read the file

        decoder = MP3Decoder(input_stream)

        # Create the chunks

        chunks: Dict[str, Chunk] = {}

        chunks[FormatChunk.HEADER_FORMAT] = FormatChunk(
            WaveFormat.PCM, False, decoder.num_channels, decoder.sample_rate, 16
        )
        chunks[DataChunk.HEADER_DATA] = DataChunk(
            np.fromstring(b"".join(decoder), dtype=np.dtype("<i2"))
        )

        # Generate the wave file and write out

        wave_file = RiffChunk(chunks)
        output_stream.write(wave_file.to_bytes())


class MpegCodec(AudioDecoder):
    """
    Uses the FFMPEG library to encode and decode.
    """

    __file_format: Literal["ogg", "flac"]
    __logger: Logger

    def __init__(self, file_format: Literal["ogg", "flac"]):
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
        return Mp3AudioDecoder()
    if "Ogg data, Vorbis audio" in mime:
        return MpegCodec("ogg")

    raise ValueError(f"{mime} is not a supported compressed audio format.")
