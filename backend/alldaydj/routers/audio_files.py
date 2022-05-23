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

from alldaydj.models.cart import CartAudio
from alldaydj.models.job import AudioUploadJob, AudioUploadStatus
from alldaydj.services.cart_repository import CartRepository
from alldaydj.services.job_repository import JobRepository
from alldaydj.services.logging import logger
from alldaydj.services.pubsub import publisher, TOPIC_VALIDATE
from alldaydj.services.storage import bucket
from fastapi import APIRouter, File, HTTPException, UploadFile
from uuid import UUID, uuid4

router = APIRouter()
cart_repository = CartRepository()
job_repository = JobRepository()


@router.get("/audio/{cart_id}")
async def get_audio(cart_id: UUID) -> CartAudio:
    if not (cart := cart_repository.get(cart_id)):
        raise HTTPException(status_code=404, detail="Cart not found")

    # Calculate the audio file URLs

    response = CartAudio()

    if cart.audio:
        response.hash_audio = cart.audio
        audio_blob = bucket.blob(cart.audio)
        response.audio = audio_blob.public_url

    if cart.compressed:
        response.hash_compressed = cart.compressed
        compressed_blob = bucket.blob(cart.audio)
        response.audio = compressed_blob.public_url

    return response


@router.post("/audio/{cart_id}")
async def upload_audio(cart_id: UUID, file: UploadFile = File(...)) -> AudioUploadJob:
    if not (cart := cart_repository.get(cart_id)):
        raise HTTPException(status_code=404, detail="Cart not found")

    # Create a job

    job_id = uuid4()
    job = AudioUploadJob(status=AudioUploadStatus.queued, cart_id=cart_id)
    job_repository.save(job_id, job)
    job.id = job_id

    # Save the file to storage

    upload_file_name = f"queued/{job.id}_{cart.id}"
    logger.info(f"Starting upload to {upload_file_name}")

    upload_blob = bucket.blob(upload_file_name)
    upload_blob.upload_from_file(file.file)
    logger.info(f"Successfully completed upload to {upload_file_name}")

    # Trigger the ingestion process

    publisher.publish(TOPIC_VALIDATE, job.json().encode("utf-8"))
    return job
