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
import magic

from alldaydj.models.job import AudioUploadJob, AudioUploadStatus, FileStage
from alldaydj.models.cart import Cart
from alldaydj.services.audio import get_wave_compression, WaveCompression
from alldaydj.services.cart_repository import CartRepository
from alldaydj.services.job_repository import JobRepository
from alldaydj.services.logging import logger
from alldaydj.services.pubsub import publisher, TOPIC_DECOMPRESS, TOPIC_METADATA
from alldaydj.services.storage import bucket
from google.cloud.functions import Context
from typing import Dict

from backend.alldaydj.services.storage import move_file_in_bucket

COMPRESSED_MIME_TYPES = ["FLAC", "ID3", "AAC", "Ogg data, Vorbis audio"]

job_repository = JobRepository()


def extract_job_from_event(event: Dict) -> AudioUploadJob:
    return AudioUploadJob(base64.b64decode(event["data"]).decode("utf-8"))


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


def validate_audio_upload(event: Dict, context: Context):
    logger.info(f"Audio validation triggered by message ID {context.event_id}")
    job = extract_job_from_event(event)
    update_job(job, AudioUploadStatus.validating)

    # Generate the source and destination filenames

    inbound_file_name = generate_file_name(job, FileStage.QUEUED)
    uncompressed_file_name = generate_file_name(job, FileStage.AUDIO)

    # Determine file type from magic bytes

    file_blob = bucket.blob(inbound_file_name)
    file_contents = file_blob.download_as_bytes()
    mime = magic.from_buffer(file_contents)

    if "WAVE audio" in mime:

        # We still need to check for compression

        compression = get_wave_compression(file_contents)
        match compression:
            case WaveCompression.COMPRESSED:
                logger.warning(
                    f"Audio upload job {job.id} encountered a compressed WAVE file"
                )
                set_job_error(job, "Compressed WAVE files are not supported.")
            case WaveCompression.UNCOMPRESSED:
                move_file_in_bucket(bucket, inbound_file_name, uncompressed_file_name)
                publisher.publish(TOPIC_METADATA, encode_for_sending(job))
            case _:
                logger.warning(
                    f"Audio upload job {job.id} failed to read the WAVE file"
                )
                set_job_error(job, "Failed to correctly read the WAVE format.")

    elif any(mime_type in mime for mime_type in COMPRESSED_MIME_TYPES):

        # Compressed audio - needs decompression

        logger.info(f"Audio upload job {job.id} encountered a {mime} file")
        publisher.publish(TOPIC_DECOMPRESS, encode_for_sending(job))
