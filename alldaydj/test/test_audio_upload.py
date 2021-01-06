from alldaydj.audio import FileStage, generate_file_name
from alldaydj.models import Artist, AudioUploadJob, Cart, Tag, Type
from alldaydj.tasks import (
    validate_audio_upload,
    decompress_audio,
    extract_audio_metadata,
)
from alldaydj.test.test_0000_init_tenancies import SetupTests
from alldaydj.test.utils import (
    set_bearer_token,
    create_tenancy,
    create_tenant_user,
)
from celery.result import EagerResult
from django.urls import reverse
from django_tenants.utils import tenant_context
from io import BytesIO
import json
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import ANY, Mock, patch
from uuid import UUID


class AudioUploadTests(APITestCase):
    """
    Test cases for the audio upload process.
    """

    USERNAME = "upload@example.com"
    PASSWORD = "$up3rS3cur3"
    TENANCY_NAME = "upload"

    @classmethod
    def setUpClass(cls):

        super(AudioUploadTests, cls).setUpClass()

        # Create the tenancy

        with tenant_context(SetupTests.PUBLIC_TENANT):
            (fqdn, tenancy) = create_tenancy(
                cls.TENANCY_NAME, SetupTests.ADMIN_USERNAME
            )
            cls.fqdn = fqdn
            cls.tenancy = tenancy

            # Create our test user

            create_tenant_user(cls.USERNAME, cls.PASSWORD, cls.TENANCY_NAME)

        # Create a test cart

        with tenant_context(cls.tenancy):

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

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("audio", kwargs={"pk": "00000000-0000-0000-0000-000000000000"})

        #  Act

        response = self.client.post(
            url, audio_request, format="multipart", **{"HTTP_HOST": self.fqdn}
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_file(self):
        """
        Tests that uploading with no file errors.
        """

        # Arrange

        audio_request = {}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("audio", kwargs={"pk": self.cart.id})

        #  Act

        response = self.client.post(
            url, audio_request, format="multipart", **{"HTTP_HOST": self.fqdn}
        )

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

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("audio", kwargs={"pk": self.cart.id})

        # Act

        response = self.client.post(
            url, audio_request, format="multipart", **{"HTTP_HOST": self.fqdn}
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        job_id = json_response["id"]
        job = AudioUploadJob.objects.get(id=job_id)

        self.assertEqual(json_response["cart"], str(self.cart.id))
        self.assertEqual(json_response["status"], "QUEUED")

        storage_mock.assert_called_with(
            generate_file_name(job, self.tenancy, FileStage.QUEUED),
            ANY,
        )

        validate_mock.assert_called_with(args=(UUID(job_id), self.TENANCY_NAME))

    def _create_job(self) -> AudioUploadJob:
        """
        Creates a new audio upload job.

        Returns:
            AudioUploadJob: The job we created.
        """

        with tenant_context(self.tenancy):
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
        storage_file_name = generate_file_name(job, self.tenancy, FileStage.QUEUED)
        expected_mime_error = f"{mime} is not a valid audio file MIME type."

        # Act

        result = validate_audio_upload.apply(args=(job.id, self.TENANCY_NAME))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(result.result, expected_mime_error)
        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.ERROR)
        self.assertEqual(updated_job.error, expected_mime_error)
        open_mock.assert_called_with(storage_file_name, "rb")
        delete_mock.assert_called_with(storage_file_name)

    @parameterized.expand(
        [
            ("./alldaydj/test/files/valid.mp3"),
            ("./alldaydj/test/files/valid.ogg"),
            ("./alldaydj/test/files/valid.flac"),
            ("./alldaydj/test/files/valid.m4a"),
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
        storage_file_name = generate_file_name(job, self.tenancy, FileStage.QUEUED)

        # Act

        validate_audio_upload.apply(args=(job.id, self.TENANCY_NAME))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        compression_mock.assert_called_with(args=(job.id, self.TENANCY_NAME))
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
        storage_file_name = generate_file_name(job, self.tenancy, FileStage.QUEUED)

        # Act

        validate_audio_upload.apply(args=(job.id, self.TENANCY_NAME))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        extract_metadata_mock.assert_called_with(args=(job.id, self.TENANCY_NAME))
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
        delete_file_name = generate_file_name(job, self.tenancy, FileStage.QUEUED)

        # Act

        decompress_audio.apply(args=(job.id, self.TENANCY_NAME, mime))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(
            updated_job.status, AudioUploadJob.AudioUploadStatus.DECOMPRESSING
        )
        extract_metadata_mock.assert_called_with(args=(job.id, self.TENANCY_NAME))
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

        result = decompress_audio.apply(args=(job.id, self.TENANCY_NAME, mime))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.ERROR)
        self.assertEqual(result.result, "Failed to decompress the audio.")

    @parameterized.expand(
        [("./alldaydj/test/files/valid_with_markers.wav", 0, 0, 41373, 0, 0)]
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

        extract_audio_metadata.apply(args=(job.id, self.TENANCY_NAME))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.METADATA)
        self.assertEqual(updated_job.cart.cue_audio_start, expected_audio_start)
        self.assertEqual(updated_job.cart.cue_intro_start, expected_intro_start)
        self.assertEqual(updated_job.cart.cue_intro_end, expected_intro_end)
        self.assertEqual(updated_job.cart.cue_segue, expected_segue)
        self.assertEqual(updated_job.cart.cue_audio_end, expected_audio_end)
        generate_compressed_audio_mock.assert_called_with(
            args=(job.id, self.TENANCY_NAME)
        )

    @parameterized.expand([("./alldaydj/test/files/valid_no_markers.wav")])
    @patch("alldaydj.tasks.generate_compressed_audio.apply_async")
    @patch("django.core.files.storage.default_storage.open")
    def test_extract_metadata(
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

        extract_audio_metadata.apply(args=(job.id, self.TENANCY_NAME))
        updated_job = AudioUploadJob.objects.get(id=job.id)

        # Assert

        self.assertEqual(updated_job.status, AudioUploadJob.AudioUploadStatus.METADATA)
        generate_compressed_audio_mock.assert_called_with(
            args=(job.id, self.TENANCY_NAME)
        )
