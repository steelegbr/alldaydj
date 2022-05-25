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

from alldaydj.models.job import AudioUploadJob, AudioUploadStatus
from alldaydj.services.job_repository import JobRepository
from alldaydj.services.storage import bucket, delete_file, file_exists, upload_file
from audio_processing import decompress_audio, validate_audio_upload
from base64 import b64encode
from parameterized import parameterized
from typing import Dict
from unittest.mock import patch
from uuid import uuid4, UUID

MODULE_NAME = "audio_processing"

job_repository = JobRepository()


class Context:
    event_id: UUID


def encode_job(job: AudioUploadJob) -> bytes:
    return job.json().encode("utf-8")


def b64_encode_job(job: AudioUploadJob):
    return b64encode(encode_job(job))


def job_to_event(job: AudioUploadJob) -> Dict:
    return {"data": b64_encode_job(job)}


def generate_context() -> Context:
    context = Context()
    context.event_id = uuid4()
    return context


@parameterized.expand(
    [
        (
            "./test/files/invalid_type.txt",
            "ASCII text, with no line terminators",
        )
    ]
)
@patch(f"{MODULE_NAME}.publisher")
def test_validate_invalid_file(file_name: str, expected_mime: str, mock_publisher):
    # Arrange

    job_id = uuid4()
    cart_id = uuid4()
    path_in_bucket = f"queued/{job_id}_{cart_id}"

    with open(file_name, "rb") as file_to_upload:
        upload_file(bucket, path_in_bucket, file_to_upload)

    job = AudioUploadJob(id=job_id, status=AudioUploadStatus.queued, cart_id=cart_id)
    event = job_to_event(job)
    context = generate_context()

    # Act

    validate_audio_upload(event, context)
    job_from_db = job_repository.get(job_id)

    # Assert

    assert job_from_db.status == AudioUploadStatus.error
    assert expected_mime in job_from_db.error
    assert not file_exists(bucket, path_in_bucket)
    mock_publisher.publish.assert_not_called()

    # Cleanup

    job_repository.delete(job_id)


@parameterized.expand(
    [
        ("./test/files/valid.mp3", True),
        ("./test/files/valid.ogg", True),
        ("./test/files/valid.flac", True),
        ("./test/files/valid.m4a", True),
        ("./test/files/valid_no_markers.wav", False),
    ]
)
@patch(f"{MODULE_NAME}.publisher")
@patch(f"{MODULE_NAME}.TOPIC_DECOMPRESS", "DECOMPRESS")
@patch(f"{MODULE_NAME}.TOPIC_METADATA", "METADATA")
def test_validate_file(file_name: str, compressed: bool, mock_publisher):
    # Arrange

    job_id = uuid4()
    cart_id = uuid4()
    path_in_bucket = f"queued/{job_id}_{cart_id}"
    decompressed_path = f"audio/{cart_id}"

    with open(file_name, "rb") as file_to_upload:
        upload_file(bucket, path_in_bucket, file_to_upload)

    job = AudioUploadJob(id=job_id, status=AudioUploadStatus.queued, cart_id=cart_id)
    event = job_to_event(job)
    context = generate_context()
    expected_message_call = encode_job(
        AudioUploadJob(id=job_id, status=AudioUploadStatus.validating, cart_id=cart_id)
    )

    # Act

    validate_audio_upload(event, context)
    job_from_db = job_repository.get(job_id)

    # Assert

    assert job_from_db.status == AudioUploadStatus.validating

    if compressed:
        assert file_exists(bucket, path_in_bucket)
        mock_publisher.publish.assert_called_with("DECOMPRESS", expected_message_call)
    else:
        assert not file_exists(bucket, path_in_bucket)
        assert file_exists(bucket, decompressed_path)
        mock_publisher.publish.assert_called_with("METADATA", expected_message_call)

    # Cleanup

    if compressed:
        delete_file(bucket, path_in_bucket)
    else:
        delete_file(bucket, decompressed_path)

    job_repository.delete(job_id)


@parameterized.expand(
    [
        ("./test/files/valid.mp3",),
        ("./test/files/valid.ogg",),
        ("./test/files/valid.flac",),
        ("./test/files/valid.m4a",),
    ]
)
@patch(f"{MODULE_NAME}.TOPIC_METADATA", "METADATA")
@patch(f"{MODULE_NAME}.publisher")
def test_decompress_audio_valid(file_name: str, mock_publisher):
    # Arrange

    job_id = uuid4()
    cart_id = uuid4()
    compressed_path = f"queued/{job_id}_{cart_id}"
    decompressed_path = f"audio/{cart_id}"

    with open(file_name, "rb") as file_to_upload:
        upload_file(bucket, compressed_path, file_to_upload)

    job = AudioUploadJob(
        id=job_id, status=AudioUploadStatus.validating, cart_id=cart_id
    )
    event = job_to_event(job)
    context = generate_context()
    expected_message_call = encode_job(
        AudioUploadJob(
            id=job_id, status=AudioUploadStatus.decompressing, cart_id=cart_id
        )
    )

    # Act

    decompress_audio(event, context)

    # Assert

    assert file_exists(bucket, decompressed_path)
    mock_publisher.publish.assert_called_with("METADATA", expected_message_call)

    # Cleanup

    delete_file(bucket, decompressed_path)
    job_repository.delete(job_id)
