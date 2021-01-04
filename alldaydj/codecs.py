from abc import ABC, abstractmethod
import ffmpeg
import numpy as np
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

    __file_format : Literal["ogg", "flac"]

    def __init__(self, file_format: Literal["ogg", "flac"]):
        self.__file_format = file_format

    def decode(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:

        # Write our inbound (compressed) file to a temporary destination

        with NamedTemporaryFile(suffix=f".{self.__file_format}", delete=False) as temp_file:
            input_stream.seek(0)
            temp_file.write(input_stream.read())
            temp_file.flush()

            # Convert

            processor, _ = (
                ffmpeg.input(temp_file.name)
                .output("pipe:", format="s16le", acodec="pcm_s16le", ar="44100")
                .run(capture_stdout=True)
            )

            output_stream.write(processor.stdout.read())


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
