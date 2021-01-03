from abc import ABC, abstractmethod
import numpy as np
from streamp3 import MP3Decoder
from typing import BinaryIO, Dict
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
    def decode(self, input: BinaryIO, output: BinaryIO) -> bool:
        pass


class Mp3AudioDecoder(AudioDecoder):
    """
    LAME based MP3 audio decoder.
    """

    def decode(self, input: BinaryIO, output: BinaryIO) -> bool:
        try:

            # Read the file

            decoder = MP3Decoder(input)

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
            output.write(wave_file.to_bytes())

        except Exception:
            return False

        return True


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

    raise ValueError(f"{mime} is not a supported compressed audio format.")
