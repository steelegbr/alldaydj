"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2022 Marc Steele
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

import base64
import json

from alldaydj.models.job import AudioUploadJob, AudioUploadStatus, FileStage
from alldaydj.services.audio import (
    get_cart_chunk,
    get_wave_compression,
    timer_to_milliseconds,
    WaveCompression,
)
from alldaydj.services.cart_repository import CartRepository
from alldaydj.services.codec import get_decoder, OggEncoder
from alldaydj.services.file import get_mime_type
from alldaydj.services.hash import generate_hash
from alldaydj.services.job_repository import JobRepository
from alldaydj.services.logging import logger
from alldaydj.services.pubsub import (
    publisher,
    TOPIC_COMPRESS,
    TOPIC_DECOMPRESS,
    TOPIC_HASHES,
    TOPIC_METADATA,
)
from alldaydj.services.storage import (
    bucket,
    delete_file,
    move_file_in_bucket,
    download_file,
    upload_file,
)
from io import BytesIO
from typing import Dict

COMPRESSED_MIME_TYPES = ["FLAC", "ID3", "AAC", "Ogg data, Vorbis audio"]
OGG_QUALITY = 4

cart_repository = CartRepository()
job_repository = JobRepository()


def extract_job_from_event(event: Dict) -> AudioUploadJob:
    json_string = base64.b64decode(event["data"]).decode("utf-8")
    json_decoded = json.loads(json_string)
    return AudioUploadJob(**json_decoded)


def encode_for_sending(job: AudioUploadJob) -> str:
    return job.json().encode("utf-8")


def generate_file_name(job: AudioUploadJob, stage: FileStage) -> str:
    match stage:
        case FileStage.QUEUED:
            return f"queued/{job.id}_{job.cart_id}"
        case FileStage.COMPRESSED:
            return f"compressed/{job.cart_id}"
        case _:
            return f"audio/{job.cart_id}"


def update_job(job: AudioUploadJob, status: AudioUploadStatus):
    job_id = job.id
    job.status = status
    job_repository.save(job_id, job)
    job.id = job_id


def set_job_error(job: AudioUploadJob, error: str):
    job.status = AudioUploadStatus.error
    job.error = error
    job_repository.save(job.id, job)


def validate_audio_upload(event: Dict, context):
    logger.info(f"Audio validation triggered by message ID {context.event_id}")
    job = extract_job_from_event(event)
    update_job(job, AudioUploadStatus.validating)

    # Generate the source and destination filenames

    inbound_file_name = generate_file_name(job, FileStage.QUEUED)
    uncompressed_file_name = generate_file_name(job, FileStage.AUDIO)

    # Determine file type from magic bytes

    file_contents = download_file(bucket, inbound_file_name)
    mime = get_mime_type(file_contents)

    if "WAVE audio" in mime:

        # We still need to check for compression

        compression = get_wave_compression(file_contents)
        match compression:
            case WaveCompression.COMPRESSED:
                logger.warning(
                    f"Audio upload job {job.id} encountered a compressed WAVE file"
                )
                delete_file(bucket, inbound_file_name)
                set_job_error(job, "Compressed WAVE files are not supported.")
            case WaveCompression.UNCOMPRESSED:
                move_file_in_bucket(bucket, inbound_file_name, uncompressed_file_name)
                publisher.publish(TOPIC_METADATA, encode_for_sending(job))
            case _:
                logger.warning(
                    f"Audio upload job {job.id} failed to read the WAVE file"
                )
                delete_file(bucket, inbound_file_name)
                set_job_error(job, "Failed to correctly read the WAVE format.")

    elif any(mime_type in mime for mime_type in COMPRESSED_MIME_TYPES):

        # Compressed audio - needs decompression

        logger.info(f"Audio upload job {job.id} encountered a {mime} file")
        publisher.publish(TOPIC_DECOMPRESS, encode_for_sending(job))

    else:

        # Bad file - stop the job and delete

        logger.warning(f"Audio upload job encountered a {mime} file")
        delete_file(bucket, inbound_file_name)
        set_job_error(job, f"{mime} is not a valid audio file MIME type")


def decompress_audio(event: Dict, context):
    logger.info(f"Audio decompression triggered by message ID {context.event_id}")
    job = extract_job_from_event(event)
    update_job(job, AudioUploadStatus.decompressing)

    compressed_file_name = generate_file_name(job, FileStage.QUEUED)
    uncompressed_file_name = generate_file_name(job, FileStage.AUDIO)

    compressed_contents = download_file(bucket, compressed_file_name)
    compressed_file = BytesIO(compressed_contents)
    uncompressed_file = BytesIO()

    try:
        get_decoder(get_mime_type(compressed_contents)).decode(
            compressed_file, uncompressed_file
        )
    except Exception as ex:
        logger.warning(f"Failed to decompress audio for job {job.id}. Details: {ex}")
        set_job_error(job, "Failed to decompress the audio")
        return

    upload_file(bucket, uncompressed_file_name, uncompressed_file)
    delete_file(bucket, compressed_file_name)

    publisher.publish(TOPIC_METADATA, encode_for_sending(job))


def extract_audio_metadata(event: Dict, context):
    logger.info(f"Metadata extraction triggered by message ID {context.event_id}")
    job = extract_job_from_event(event)
    update_job(job, AudioUploadStatus.metadata)

    audio_file_name = generate_file_name(job, FileStage.AUDIO)
    audio_contents = download_file(bucket, audio_file_name)
    audio_file = BytesIO(audio_contents)

    (cart_chunk, format_chunk) = get_cart_chunk(audio_file)
    if cart_chunk:
        logger.info(f"Updating cart {job.cart_id} with cart chunk data")
        cart = cart_repository.get_by_id(job.cart_id)
        cart.cue_audio_start = timer_to_milliseconds(
            cart_chunk, format_chunk, ["AUD1", "AUDs"]
        )
        cart.cue_intro_end = timer_to_milliseconds(
            cart_chunk, format_chunk, ["INT", "INT2", "INTe"]
        )
        cart.cue_segue = timer_to_milliseconds(
            cart_chunk, format_chunk, ["SEG ", "SEG1", "SEGs"]
        )
        cart.cue_audio_end = timer_to_milliseconds(
            cart_chunk, format_chunk, ["AUD2", "AUDe"]
        )
        cart_repository.save(cart)

    publisher.publish(TOPIC_COMPRESS, encode_for_sending(job))


def generate_compressed_audio(event: Dict, context):
    logger.info(f"Audio compression triggered by message ID {context.event_id}")
    job = extract_job_from_event(event)
    update_job(job, AudioUploadStatus.compressing)

    uncompressed_file_name = generate_file_name(job, FileStage.AUDIO)
    compressed_file_name = generate_file_name(job, FileStage.COMPRESSED)

    uncompressed_contents = download_file(bucket, uncompressed_file_name)
    uncompressed_blob = BytesIO(uncompressed_contents)
    compressed_blob = BytesIO()

    OggEncoder().encode(uncompressed_blob, compressed_blob, OGG_QUALITY)
    upload_file(bucket, compressed_file_name, compressed_blob)

    publisher.publish(TOPIC_HASHES, encode_for_sending(job))


def generate_hashes(event: Dict, context):
    logger.info(f"Hash generation triggered by message ID {context.event_id}")
    job = extract_job_from_event(event)
    update_job(job, AudioUploadStatus.hashing)

    uncompressed_file_name = generate_file_name(job, FileStage.AUDIO)
    compressed_file_name = generate_file_name(job, FileStage.COMPRESSED)

    uncompressed_contents = download_file(bucket, uncompressed_file_name)
    compressed_contents = download_file(bucket, compressed_file_name)

    cart = cart_repository.get_by_id(job.cart_id)
    cart.hash_audio = generate_hash(uncompressed_contents)
    cart.hash_compressed = generate_hash(compressed_contents)
    cart.audio = uncompressed_file_name
    cart.compressed = compressed_file_name
    cart_repository.save(cart)

    update_job(job, AudioUploadStatus.done)
