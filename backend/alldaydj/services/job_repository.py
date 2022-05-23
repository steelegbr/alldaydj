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
from alldaydj.services.database import db, strip_id
from alldaydj.services.logging import logger
from alldaydj.services.repository import Repository
from typing import Optional
from uuid import UUID

COLLECTION_JOB = "jobs"


class JobRepository(Repository):
    def __map_doc_to_job(self, job_doc) -> AudioUploadJob:
        return AudioUploadJob.parse_obj({**job_doc.to_dict(), "id": job_doc.id})

    def get(self, id: UUID) -> Optional[AudioUploadJob]:
        logger.info(f"Lookup for job ID {id}")
        return self.get_document(id, COLLECTION_JOB, self.__map_doc_to_job)

    def save(self, id: UUID, job: AudioUploadJob):
        logger.info(f"Saving job {id}")
        self.save_stripped_document(
            id, COLLECTION_JOB, job, {"cart_id": str(job.cart_id)}
        )
