from alldaydj.codecs import get_decoder, OggEncoder
from io import BytesIO
import magic
from parameterized import parameterized
from unittest import TestCase


class TestCodecs(TestCase):
    """
    Tests audio CODECs.
    """

    @parameterized.expand(
        [
            (
                "./alldaydj/test/files/valid.mp3",
                "./alldaydj/test/files/valid_mp3_decoded.wav",
            ),
            (
                "./alldaydj/test/files/valid.ogg",
                "./alldaydj/test/files/valid_ogg_decoded.wav",
            ),
            (
                "./alldaydj/test/files/valid.flac",
                "./alldaydj/test/files/valid_flac_decoded.wav",
            ),
            (
                "./alldaydj/test/files/valid.m4a",
                "./alldaydj/test/files/valid_m4a_decoded.wav",
            ),
        ]
    )
    def test_codec_valid(self, source_file: str, expected_file: str):
        """
        CODECs successfully decode.
        """

        # Arrange

        with open(source_file, "rb") as source:
            with open(expected_file, "rb") as expected:
                in_memory = BytesIO(bytes([0] * len(expected.read())))
                mime = magic.from_buffer(source.read(1024))

                # Act

                get_decoder(mime).decode(source, in_memory)
                in_memory.seek(0)
                expected.seek(0)

                # Assert

                self.assertEqual(len(in_memory.read()), len(expected.read()))

    @parameterized.expand(
        [
            (
                "./alldaydj/test/files/valid_with_markers.wav",
                "./alldaydj/test/files/compressed.ogg",
            ),
        ]
    )
    def test_ogg_encode(self, source_file: str, expected_file: str):
        """
        OGG encoding works.
        """

        # Arrange

        with open(source_file, "rb") as source, open(expected_file, "rb") as expected:
            in_memory = BytesIO(bytes([0] * len(expected.read())))

            # Act

            OggEncoder().encode(source, in_memory, 4)
            in_memory.seek(0)
            expected.seek(0)

            # Assert

            self.assertEqual(len(in_memory.read()), len(expected.read()))
