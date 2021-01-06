import hashlib
from typing import BinaryIO


def generate_hash(byte_stream: BinaryIO) -> str:
    """
    Generates a SHA256 hash of a given byte stream.

    Args:
        byte_stream (BinaryIO): The stream to get the hash of.

    Returns:
        str: The SHA256 hash.
    """
    byte_stream.seek(0)
    hashed_stream = hashlib.sha256(byte_stream.read())
    return hashed_stream.hexdigest()
