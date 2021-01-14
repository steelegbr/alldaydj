from alldaydj.hash import generate_hash
from parameterized import parameterized
from unittest import TestCase


class TestHash(TestCase):
    """
    Tests hashing functions.
    """

    @parameterized.expand(
        [
            (
                "./alldaydj/test/files/valid.ogg",
                "b9452aaeb14828fe7c9cae6749878220a26977963f91471a0193c75c59081e86",
            ),
            (
                "./alldaydj/test/files/valid_with_markers.wav",
                "d6e4085fffc29e8bcc526ae32446f779f05fa2ecaf17f3e8b4584bee02079f88",
            ),
        ]
    )
    def test_hash(self, file_name: str, expected_hash: str):
        """
        Generate SHA256 hashes correctly.
        """

        # Arrange

        with open(file_name, "rb") as file_to_hash:

            # Act

            hashed_file = generate_hash(file_to_hash)

            # Assert

            self.assertEqual(hashed_file, expected_hash)
