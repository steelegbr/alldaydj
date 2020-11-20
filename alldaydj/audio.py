"""
    Audio Utility Methods
"""

from alldaydj.tenants.models import Tenant
from alldaydj.models import AudioUploadJob
from chunk import Chunk
from enum import Enum
from typing import BinaryIO


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

    while True:
        try:
            chunk = Chunk(file)
            if chunk.getname() == "fmt ":
                data = chunk.read()
                if data[8:9] == 1:
                    return WaveCompression.UNCOMPRESSED
                return WaveCompression.COMPRESSED

        except EOFError:

            # If we get here we didn't see a format chunk

            return WaveCompression.INVALID


class FileStage(Enum):
    """
    The possible stages an audio file can be in.
    """

    QUEUED = 0
    COMPRESSED = 1
    AUDIO = 2


def generate_file_name(job: AudioUploadJob, tenant: Tenant, stage: FileStage) -> str:
    """
    Generates the name of an audio file based on the stage.

    Args:
        job_id (AudioUploadJob): The job we're doing this for.
        tenant (Tenant): The tenant we're managing the file for.
        stage (FileStage): The stage the file is in.

    Returns:
        str: The file name.
    """

    if stage == FileStage.QUEUED:
        return f"queued/{tenant.name}_{job.id}_{job.cart.id}"
    elif stage == FileStage.COMPRESSED:
        return f"compressed/{tenant.name}_{job.cart.id}"

    return f"audio/{tenant.name}_{job.cart.id}"
