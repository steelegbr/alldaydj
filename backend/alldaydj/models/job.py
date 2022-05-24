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

from enum import Enum
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class AudioUploadStatus(str, Enum):
    queued = "QUEUED"
    error = "ERROR"
    validating = "VALIDATING"
    decompressing = "DECOMPRESSING"
    metadata = "METADATA"
    compressing = "COMPRESSING"
    hashing = "HASHING"
    done = "DONE"


class AudioUploadJob(BaseModel):
    id: Optional[UUID]
    status: AudioUploadStatus
    cart_id: UUID
    error: Optional[str]


class FileStage(Enum):
    QUEUED = 0
    COMPRESSED = 1
    AUDIO = 2
