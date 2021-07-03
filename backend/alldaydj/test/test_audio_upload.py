"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

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

from alldaydj.audio import FileStage, generate_file_name
from alldaydj.models import Artist, AudioUploadJob, Cart, Tag, Type
from alldaydj.tasks import (
    validate_audio_upload,
    decompress_audio,
    extract_audio_metadata,
    generate_compressed_audio,
    generate_hashes,
)
from alldaydj.test.utils import set_bearer_token
from django.contrib.auth.models import User
from django.urls import reverse
from io import BytesIO
import json
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, ANY
from uuid import UUID


class AudioUploadTests(APITestCase):
    """
    Test cases for the audio upload process.
    """

    USERNAME = "upload@example.com"
    PASSWORD = "$up3rS3cur3"

    @classmethod
    def setUpClass(cls):

        super(AudioUploadTests, cls).setUpClass()

        #  Create our test user

        User.objects.create_user(username=cls.USERNAME, password=cls.PASSWORD)

        # Create a test cart

        artist = Artist(name="Test Artist")
        artist.save()

        tag = Tag(tag="Test Tag")
        tag.save()

        cart_type = Type(name="Test Type")
        cart_type.save()

        cls.cart = Cart(
            label="TEST123",
            title="Test Cart",
            display_artist="Test Artist",
            cue_audio_start=0,
            cue_audio_end=0,
            cue_intro_start=0,
            cue_intro_end=0,
            cue_segue=0,
            sweeper=False,
            year=2020,
            isrc="ISRC123",
            composer="Composer Name",
            publisher="Publisher Name",
            record_label="Record Label",
            type=cart_type,
        )

        cls.cart.artists.set([artist])
        cls.cart.tags.set([tag])
        cls.cart.save()

    def test_bad_cart(self):
        """
        Tests we can't upload to a bad (non-existant) cart.
        """

        # Arrange

        audio_request = {"file": "RIFFTESTFILE"}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("audio", kwargs={"pk": "00000000-0000-0000-0000-000000000000"})

        #  Act

        response = self.client.post(url, audio_request, format="multipart")

        # Assert

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_file(self):
        """
        Tests that uploading with no file errors.
        """

        # Arrange

        audio_request = {}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("audio", kwargs={"pk": self.cart.id})

        #  Act

        response = self.client.post(url, audio_request, format="multipart")

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode(), "You must upload an audio file to process."
        )

    @parameterized.expand(
        [
            ("./alldaydj/test/files/valid_no_markers.wav"),
            ("./alldaydj/test/files/valid.mp3"),
        ]
    )
    @patch("alldaydj.tasks.validate_audio_upload.apply_async")
    @patch("django.core.files.storage.default_storage.save")
    def test_trigger_upload(self, file_name: str, storage_mock, validate_mock):
        """
        Tests a file upload trigger the process.
        """

        # Arrange

        audio_request = {"file": open(file_name, "rb")}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("audio", kwargs={"pk": self.cart.id})

        # Act

        response = self.client.post(url, audio_request, format="multipart")

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        job_id = json_response["id"]
        job = AudioUploadJob.objects.get(id=job_id)

        self.assertEqual(json_response["cart"], str(self.cart.id))
        self.assertEqual(json_response["status"], "QUEUED")

        storage_mock.assert_called_with(
            generate_file_name(job, FileStage.QUEUED),
            ANY,
        )

        validate_mock.assert_called_with(args=(UUID(job_id),))

    def _create_job(self) -> AudioUploadJob:
        """
        Creates a new audio upload job.

        Returns:
            AudioUploadJob: The job we created.
        """

        job = AudioUploadJob(cart=self.cart)
        job.save()

        return job

    @parameterized.expand(
        [
            (
                "./alldaydj/test/files/invalid_type.txt",
                "ASCII text, with no line terminators",
            )
        ]
    )
    @patch("django.core.files.storage.default_storage.delete")
    @patch("django.core.files.storage.default_storage.open")
    def test_validate_invalid_file(
        self, file_name: str, mime: str, open_mock, delete_mock
    ):
        """
        Tests invalid files don't make it past validation.
        """

        # Arrange

        job = self._create_job()
        open_mock.return_value = open(file_name, "rb")
        storage_file_name = generate_file_name(job, FileStage.QUEUED)
        expected_mime_error = f"{mime} is not a valid audio file MIME type."

        # Act

        result = validate_audio_upload.apply(args=(job.id,))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(result.result, expected_mime_error)
        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.ERROR)
        self.assertEqual(updated_job.error, expected_mime_error)
        open_mock.assert_called_with(storage_file_name, "rb")
        delete_mock.assert_called_with(storage_file_name)

    @parameterized.expand(
        [
            ("./alldaydj/test/files/valid.mp3",),
            ("./alldaydj/test/files/valid.ogg",),
            ("./alldaydj/test/files/valid.flac",),
            ("./alldaydj/test/files/valid.m4a",),
        ]
    )
    @patch("alldaydj.tasks.decompress_audio.apply_async")
    @patch("django.core.files.storage.default_storage.open")
    def test_validate_compressed_file(
        self, file_name: str, open_mock, compression_mock
    ):
        """
        Compressed files pass validation and gets assigned for decompression.
        """

        # Arrange

        job = self._create_job()
        open_mock.return_value = open(file_name, "rb")
        storage_file_name = generate_file_name(job, FileStage.QUEUED)

        # Act

        validate_audio_upload.apply(args=(job.id,))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        compression_mock.assert_called()
        self.assertEqual(
            updated_job.status, AudioUploadJob.AudioUploadStatus.VALIDATING
        )
        open_mock.assert_called_with(storage_file_name, "rb")

    @parameterized.expand(
        [
            ("./alldaydj/test/files/valid_no_markers.wav"),
        ]
    )
    @patch("alldaydj.tasks._move_audio_file")
    @patch("alldaydj.tasks.extract_audio_metadata.apply_async")
    @patch("django.core.files.storage.default_storage.open")
    def test_validate_uncompressed_file(
        self, file_name: str, open_mock, extract_metadata_mock, move_audio_mock
    ):
        """
        Uncompressed audio files pass validation.
        """

        # Arrange

        job = self._create_job()
        open_mock.return_value = open(file_name, "rb")
        storage_file_name = generate_file_name(job, FileStage.QUEUED)

        # Act

        validate_audio_upload.apply(args=(job.id,))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        extract_metadata_mock.assert_called_with(args=(job.id,))
        self.assertEqual(
            updated_job.status, AudioUploadJob.AudioUploadStatus.VALIDATING
        )
        open_mock.assert_called_with(storage_file_name, "rb")

    @parameterized.expand(
        [
            ("./alldaydj/test/files/valid.mp3", "ID3"),
            ("./alldaydj/test/files/valid.ogg", "Ogg data, Vorbis audio"),
            ("./alldaydj/test/files/valid.flac", "FLAC"),
            ("./alldaydj/test/files/valid.m4a", "AAC"),
        ]
    )
    @patch("alldaydj.tasks.extract_audio_metadata.apply_async")
    @patch("django.core.files.storage.default_storage.delete")
    @patch("django.core.files.storage.default_storage.open")
    def test_decompress_audio_valid(
        self, file_name: str, mime: str, open_mock, delete_mock, extract_metadata_mock
    ):
        """
        Audio decompression task.
        """

        # Arrange

        job = self._create_job()
        open_mock.side_effect = [open(file_name, "rb"), BytesIO()]
        delete_file_name = generate_file_name(job, FileStage.QUEUED)

        # Act

        decompress_audio.apply(args=(job.id, mime))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(
            updated_job.status, AudioUploadJob.AudioUploadStatus.DECOMPRESSING
        )
        extract_metadata_mock.assert_called_with(args=(job.id,))
        delete_mock.assert_called_with(delete_file_name)

    @parameterized.expand(
        [
            ("./alldaydj/test/files/invalid_type.txt", "AAC"),
        ]
    )
    @patch("django.core.files.storage.default_storage.open")
    def test_decompress_audio_invalid(self, file_name: str, mime: str, open_mock):
        """
        Audio decompression failure.
        """

        # Arrange

        job = self._create_job()
        open_mock.side_effect = [open(file_name, "rb"), BytesIO()]

        # Act

        result = decompress_audio.apply(args=(job.id, mime))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.ERROR)
        self.assertEqual(result.result, "Failed to decompress the audio.")

    @parameterized.expand(
        [("./alldaydj/test/files/valid_with_markers.wav", 0, 0, 938, 2451, 0)]
    )
    @patch("alldaydj.tasks.generate_compressed_audio.apply_async")
    @patch("django.core.files.storage.default_storage.open")
    def test_extract_metadata(
        self,
        file_name: str,
        expected_audio_start: int,
        expected_intro_start: int,
        expected_intro_end: int,
        expected_segue: int,
        expected_audio_end: int,
        open_mock,
        generate_compressed_audio_mock,
    ):
        """
        Metadata successfully extracted from a file with cart chunk.
        """

        # Arrange

        job = self._create_job()
        open_mock.side_effect = [open(file_name, "rb"), BytesIO()]

        # Act

        extract_audio_metadata.apply(args=(job.id,))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.METADATA)
        self.assertEqual(updated_job.cart.cue_audio_start, expected_audio_start)
        self.assertEqual(updated_job.cart.cue_intro_start, expected_intro_start)
        self.assertEqual(updated_job.cart.cue_intro_end, expected_intro_end)
        self.assertEqual(updated_job.cart.cue_segue, expected_segue)
        self.assertEqual(updated_job.cart.cue_audio_end, expected_audio_end)
        generate_compressed_audio_mock.assert_called_with(args=(job.id,))

    @parameterized.expand([("./alldaydj/test/files/valid_no_markers.wav")])
    @patch("alldaydj.tasks.generate_compressed_audio.apply_async")
    @patch("django.core.files.storage.default_storage.open")
    def test_extract_metadata_failure(
        self,
        file_name: str,
        open_mock,
        generate_compressed_audio_mock,
    ):
        """
        Metadata not extracted from a file with no cart chunk.
        """

        # Arrange

        job = self._create_job()
        open_mock.side_effect = [open(file_name, "rb"), BytesIO()]

        # Act

        extract_audio_metadata.apply(args=(job.id,))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.METADATA)
        generate_compressed_audio_mock.assert_called_with(args=(job.id,))

    @parameterized.expand([("./alldaydj/test/files/valid_no_markers.wav")])
    @patch("alldaydj.tasks.generate_hashes.apply_async")
    @patch("django.core.files.storage.default_storage.open")
    def test_compress_audio(self, file_name: str, open_mock, generate_hashes_mock):
        """
        Audio compression task.
        """

        # Arrange

        job = self._create_job()
        open_mock.side_effect = [open(file_name, "rb"), BytesIO()]

        # Act

        generate_compressed_audio.apply(args=(job.id,))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(
            updated_job.status, AudioUploadJob.AudioUploadStatus.COMPRESSING
        )
        generate_hashes_mock.assert_called_with(args=(job.id,))

    @parameterized.expand(
        [
            (
                "./alldaydj/test/files/valid_with_markers.wav",
                "./alldaydj/test/files/valid.ogg",
                "d6e4085fffc29e8bcc526ae32446f779f05fa2ecaf17f3e8b4584bee02079f88",
                "b9452aaeb14828fe7c9cae6749878220a26977963f91471a0193c75c59081e86",
            ),
        ]
    )
    @patch("django.core.files.storage.default_storage.open")
    def test_generate_hashes(
        self,
        audio_file_name: str,
        compressed_file_name: str,
        expected_audio_hash: str,
        expected_compressed_hash: str,
        open_mock,
    ):
        """
        Generate audio file hashes.
        """

        # Arrange

        job = self._create_job()
        open_mock.side_effect = [
            open(audio_file_name, "rb"),
            open(compressed_file_name, "rb"),
        ]

        # Act

        generate_hashes.apply(args=(job.id,))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.DONE)
        self.assertEqual(updated_job.cart.hash_audio, expected_audio_hash)
        self.assertEqual(updated_job.cart.hash_compressed, expected_compressed_hash)
