from alldaydj.models import Artist, AudioUploadJob, Cart, Tag, Type
from alldaydj.test.test_0000_init_tenancies import SetupTests
from alldaydj.test.utils import (
    set_bearer_token,
    create_tenancy,
    create_tenant_user,
)
from django.urls import reverse
from django_tenants.utils import tenant_context
import json
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
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
        Tests we can't upload to a bad (non-existant) cart
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
        Tests that uploading with no file errors
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

    @patch("alldaydj.tasks.validate_audio_upload.apply_async")
    @patch("django.core.files.storage.default_storage.save")
    def test_trigger_upload(self, storage_mock, validate_mock):
        """
        Tests a file upload trigger the process
        """

        # Arrange

        audio_request = {"file": "RIFFTESTFILE"}

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

        self.assertEqual(json_response["cart"], str(self.cart.id))
        self.assertEqual(json_response["status"], "QUEUED")

        storage_mock.assert_called_with(
            f"queued/{self.TENANCY_NAME}_{job_id}_{self.cart.id}", "RIFFTESTFILE"
        )

        validate_mock.assert_called_with(args=(UUID(job_id), self.TENANCY_NAME))
