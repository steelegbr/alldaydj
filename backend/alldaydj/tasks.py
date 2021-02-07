"""
    Async tasks for AllDay DJ.
"""

from alldaydj.models import AudioUploadJob
from alldaydj.audio import (
    FileStage,
    WaveCompression,
    get_wave_compression,
    generate_file_name,
    get_cart_chunk,
)
from alldaydj.codecs import get_decoder, OggEncoder
from alldaydj.hash import generate_hash
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.storage import default_storage
from functools import wraps
from logging import getLogger
import magic
from os import environ
from typing import Any, List, Tuple
from wave_chunk_parser.chunks import CartTimer


def __get_upload_job(job_id: str) -> AudioUploadJob:
    """
    Obtains the upload job and associated tenancy.

    Args:
        job_id (str): The job ID to search for.

    Raises:
        ValueError: Failed to get the job.

    Returns:
        AudioUploadJob: The job.
    """

    # Find the upload job

    job = AudioUploadJob.objects.filter(id=job_id).first()

    if not job:
        raise ValueError(f"Upload job {job_id} is not valid.")

    return job


def __set_job_status(
    job_id: str, status: AudioUploadJob.AudioUploadStatus
) -> AudioUploadJob:
    """
    Sets the audio upload job status.

    Args:
        job_id (str): The UUID of the job.
        status (AudioUploadJob.AudioUploadStatus): The status to set.

    Returns:
        AudioUploadJob: The job.
    """

    job = __get_upload_job(job_id)
    job.status = status
    job.save()

    return job


def _set_job_error(job: AudioUploadJob, error: str) -> str:
    """
    Sets the error on the audio upload job.

    Args:
        job (AudioUploadJob): The job to set the error on.
        error (str): The error message.
    """

    job.status = AudioUploadJob.AudioUploadStatus.ERROR
    job.error = error
    job.save()
    return error


def _move_audio_file(src: str, dst: str):
    """
    Moves an audio file in the django file store.

    Args:
        src (str): The source file name.
        dst (str): The destination file name.
    """

    logger = getLogger(__name__)

    # Check the source exists

    if not default_storage.exists(src):
        logger.error(f"Cannot move {src} to {dst} as the source file does not exist.")
        raise ValueError(f"{src} is not a valid source file name.")

    # Copy the contents

    with default_storage.open(src, "rb") as src_file:
        contents = src_file.read()

    default_storage.save(dst, contents)

    # Delete the source file

    default_storage.delete(src)
    logger.info(f"Successfully moved {src} to {dst}.")


@shared_task
def validate_audio_upload(job_id: str) -> str:
    """
    Validates an uploaded audio file.

    Args:
        job_id (str): The UUID of the job we're working on.

    Returns:
        str: The success / failure message.
    """

    job = __set_job_status(job_id, AudioUploadJob.AudioUploadStatus.VALIDATING)
    logger = getLogger(__name__)

    # Open the file and check the type

    inbound_file_name = generate_file_name(job, FileStage.QUEUED)
    uncompressed_file_name = generate_file_name(job, FileStage.AUDIO)

    with default_storage.open(inbound_file_name, "rb") as inbound_file:
        mime = magic.from_buffer(inbound_file.read(1024))
        inbound_file.seek(0)

        if "WAVE audio" in mime:

            # WAVE files - need to check if it's compressed

            compression = get_wave_compression(inbound_file)

            if compression == WaveCompression.COMPRESSED:
                logger.warning(
                    f"Audio upload job {job_id} encountered a compressed WAVE file."
                )
                return _set_job_error(job, "Compressed WAVE files are not supported.")
            if compression == WaveCompression.UNCOMPRESSED:
                logger.info(f"Audio upload job {job_id} encountered a WAVE file.")
                _move_audio_file(inbound_file_name, uncompressed_file_name)
                extract_audio_metadata.apply_async(args=(job_id,))
            elif compression == WaveCompression.INVALID:
                logger.warning(
                    f"Audio upload job {job_id} encountered a WAVE file with no format chunk."
                )
                return _set_job_error(job, "Failed to find the format chunk.")

        elif any(
            mime_type in mime for mime_type in settings.ADDJ_COMPRESSED_MIME_TYPES
        ):

            # Compressed files - re-encode

            logger.info(f"Audio upload job {job_id} encountered a {mime} file.")
            decompress_audio.apply_async(args=(job_id, mime))

        else:

            # Invalid format
            # Delete the file and note the error in the job

            default_storage.delete(inbound_file_name)
            logger.error(f"Audio upload job {job_id} encountered a {mime} file.")
            return _set_job_error(job, f"{mime} is not a valid audio file MIME type.")


@shared_task
def decompress_audio(job_id: str, mime: str):
    """
    Decompresses audio to WAVE format.

    Args:
        job_id (str): The job to perform this task for.
        mime (str): The mime type of the file.
    """

    job = __set_job_status(job_id, AudioUploadJob.AudioUploadStatus.DECOMPRESSING)
    logger = getLogger(__name__)

    # Open the files and attempt to convert

    inbound_file_name = generate_file_name(job, FileStage.QUEUED)
    uncompressed_file_name = generate_file_name(job, FileStage.AUDIO)

    with default_storage.open(
        inbound_file_name, "rb"
    ) as inbound_file, default_storage.open(
        uncompressed_file_name, "wb"
    ) as uncompressed_file:

        try:
            get_decoder(mime).decode(inbound_file, uncompressed_file)
        # skipcq: PYL-W0703
        # We just want to log something went wrong, not crash out
        except Exception as ex:
            logger.error(
                f"Failed to decompress the audio for upload job {job_id}. Details: {ex}",
            )
            return _set_job_error(job, "Failed to decompress the audio.")

    # Delete the compressed file and move onto metadata extraction

    default_storage.delete(inbound_file_name)
    extract_audio_metadata.apply_async(args=(job_id,))


def __get_timer(
    timers: List[CartTimer], possible_prefixes: List[str], sample_rate: int
):
    """
    Obtains the timer from a given list.

    Args:
        timers (List[CartTimer]): The list of timers.
        possible_prefixes (List[str]): The prefixes we're working through.
        sample_rate (int): The sample rate.
    """

    for prefix in possible_prefixes:
        if found_timers := [timer for timer in timers if timer.name == prefix]:
            return (found_timers[0].time * 1000) // sample_rate

    return 0


@shared_task
def extract_audio_metadata(job_id: str):
    """
    Attempts to extract metadata from an uncompressed audio file.

    Args:
        job_id (str): The job to perform this task for.
    """

    job = __set_job_status(job_id, AudioUploadJob.AudioUploadStatus.METADATA)
    logger = getLogger(__name__)

    audio_file_name = generate_file_name(job, FileStage.AUDIO)

    with default_storage.open(audio_file_name, "rb") as audio_file:
        (cart_chunk, format_chunk) = get_cart_chunk(audio_file)
        if cart_chunk:

            logger.info(f"Updating cart {job.cart.id} with cart chunk data.")

            # Update the timers based on the cart chunk

            job.cart.cue_audio_start = __get_timer(
                cart_chunk.timers, ["AUD1", "AUDs"], format_chunk.sample_rate
            )
            job.cart.cue_intro_start = __get_timer(
                cart_chunk.timers, ["INT1", "INTs"], format_chunk.sample_rate
            )
            job.cart.cue_intro_end = __get_timer(
                cart_chunk.timers, ["INT ", "INT2", "INTe"], format_chunk.sample_rate
            )
            job.cart.cue_segue = __get_timer(
                cart_chunk.timers, ["SEG ", "SEG1", "SEGs"], format_chunk.sample_rate
            )
            job.cart.cue_audio_end = __get_timer(
                cart_chunk.timers, ["AUD2", "AUDe"], format_chunk.sample_rate
            )

            job.cart.save()

    # Move on to generating the compressed audio file

    generate_compressed_audio.apply_async(args=(job_id,))


@shared_task
def generate_compressed_audio(job_id: str):
    """
    Generates the compressed (OGG) audio file.

    Args:
        job_id (str): The job to perform this task for.
    """

    job = __set_job_status(job_id, AudioUploadJob.AudioUploadStatus.COMPRESSING)
    logger = getLogger(__name__)

    audio_file_name = generate_file_name(job, FileStage.AUDIO)
    compressed_file_name = generate_file_name(job, FileStage.COMPRESSED)

    with default_storage.open(
        audio_file_name, "rb"
    ) as audio_file, default_storage.open(
        compressed_file_name, "wb"
    ) as compressed_file:
        logger.info(f"Compressing WAV to OGG for job {job_id}.")
        OggEncoder().encode(audio_file, compressed_file, settings.ADDJ_OGG_QUALITY)

    generate_hashes.apply_async(args=(job_id,))


@shared_task
def generate_hashes(job_id: str):
    """
    Generates the file hashes used by clients to manage their caches.

    Args:
        job_id (str): The job to perform this task for.
    """

    job = __set_job_status(job_id, AudioUploadJob.AudioUploadStatus.HASHING)
    logger = getLogger(__name__)

    audio_file_name = generate_file_name(job, FileStage.AUDIO)
    compressed_file_name = generate_file_name(job, FileStage.COMPRESSED)

    job.cart.audio = audio_file_name
    job.cart.compressed = compressed_file_name

    with default_storage.open(
        audio_file_name, "rb"
    ) as audio_file, default_storage.open(
        compressed_file_name, "rb"
    ) as compressed_file:
        job.cart.hash_audio = generate_hash(audio_file)
        job.cart.hash_compressed = generate_hash(compressed_file)

    logger.info(f"Generated hashes for audio upload job {job_id}.")

    job.cart.save()
    __set_job_status(job_id, AudioUploadJob.AudioUploadStatus.DONE)
