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
from alldaydj.services.storage import bucket, delete_file, upload_file
from audio_processing import validate_audio_upload
from base64 import b64encode
from parameterized import parameterized
from typing import Dict
from unittest.mock import patch
from uuid import uuid4

MODULE_NAME = "audio_processing"

job_repository = JobRepository()


def job_to_event(job: AudioUploadJob) -> Dict:
    return {"data": b64encode(job.json())}


@parameterized.expand(
    [
        (
            "./test/files/invalid_type.txt",
            "ASCII text, with no line terminators",
        )
    ]
)
def test_validate_invalid_file(file_name: str, expected_mime: str):
    # Arrange

    job_id = uuid4()
    cart_id = uuid4()
    path_in_bucket = f"queued/{job_id}_{cart_id}"

    with open(file_name, "rb") as file_to_upload:
        upload_file(bucket, path_in_bucket, file_to_upload)

    job = AudioUploadJob(id=job_id, status=AudioUploadStatus.queued, cart_id=cart_id)
    event = job_to_event(job)

    # Act

    validate_audio_upload(event, None)
    job_from_db = job_repository.get(job_id)

    # Assert

    assert job_from_db.status == AudioUploadStatus.error

    # Cleanup

    delete_file(bucket, path_in_bucket)
    job_repository.delete(job_id)
