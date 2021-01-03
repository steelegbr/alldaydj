from alldaydj.codecs import get_decoder
from io import BytesIO
import magic
from parameterized import parameterized
from unittest import TestCase


class TestDecoder(TestCase):
    """
    Tests audio decoders into WAVE.
    """

    @parameterized.expand(
        [
            (
                "./alldaydj/test/files/valid.mp3",
                "./alldaydj/test/files/valid_mp3_decoded.wav",
            )
        ]
    )
    def test_codec_valid(self, source_file: str, expected_file: str):
        """
        CODECs successfully decode.

        Args:
            source_file (str): The source file to decode.
            expected_file (str): The expected output.
        """

        # Arrange

        with open(source_file, "rb") as source:
            with open(expected_file, "rb") as expected:
                in_memory = BytesIO(bytes([0] * len(expected.read())))
                mime = magic.from_buffer(source.read(1024))

                # Act

                result = get_decoder(mime).decode(source, in_memory)

                # Assert

                self.assertTrue(result)
                self.assertEqual(in_memory.read(), expected.read())
