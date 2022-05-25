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

from alldaydj.services.firebase import firebase_app
from alldaydj.services.logging import logger
from firebase_admin import storage
from os import environ
from typing import BinaryIO

bucket = storage.bucket(environ.get("ALLDAYDJ_BUCKET"))


def delete_file(bucket, path: str):
    logger.info(f"Deleting file {path} from bucket")
    delete_blob = bucket.blob(path)
    delete_blob.delete()


def move_file_in_bucket(bucket, source_path: str, dest_path: str):
    logger.info(f"Moving file in bucket from {source_path} to {dest_path}")
    source_blob = bucket.blob(source_path)
    bucket.copy_blob(source_blob, bucket, dest_path)
    source_blob.delete()


def download_file(bucket, path: str) -> bytes:
    logger.info(f"Reading file {path} from bucket")
    file_blob = bucket.blob(path)
    return file_blob.download_as_bytes()


def upload_file(bucket, path: str, contents: BinaryIO):
    logger.info(f"Uploading file path {path} to bucket")
    upload_blob = bucket.blob(path)
    contents.seek(0)
    upload_blob.upload_from_file(contents)


def file_exists(bucket, path: str) -> bool:
    logger.info(f"Checking if {path} exists in the bucket")
    file_blob = bucket.blob(path)
    return file_blob.exists()
