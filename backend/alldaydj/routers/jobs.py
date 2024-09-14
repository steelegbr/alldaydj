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

from alldaydj.models.job import AudioUploadJob
from alldaydj.services.job_repository import JobRepository
from fastapi import APIRouter, HTTPException
from uuid import UUID

router = APIRouter()
job_repository = JobRepository()


@router.get("/job/{job_id}")
def get_job(self, job_id: UUID) -> AudioUploadJob:
    if not (job := job_repository.get(job_id)):
        raise HTTPException(status_code=404, detail="Job not found")

    return job
