from alldaydj.models import Tag
from alldaydj.test.test_0000_init_tenancies import SetupTests
from alldaydj.test.utils import (
    set_bearer_token,
    create_tenancy,
    create_public_tenant,
    create_tenant_user,
)
from django.urls import reverse
from django.conf import settings
from django_tenants.utils import tenant_context
import json
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from typing import List


class TagTests(APITestCase):
    """
    Test cases for the tag management API.
    """

    ADMIN_USERNAME = "admin@example.com"
    ADMIN_PASSWORD = "1337h@x0r"
    USERNAME = "tag@example.com"
    PASSWORD = "$up3rS3cur3"
    TENANCY_NAME = "tag"

    @classmethod
    def setUpClass(cls):

        super(TagTests, cls).setUpClass()

        # Create the tenancy

        with tenant_context(SetupTests.PUBLIC_TENANT):
            create_public_tenant(cls.ADMIN_USERNAME, cls.ADMIN_PASSWORD)
            (fqdn, tenancy) = create_tenancy(cls.TENANCY_NAME, cls.ADMIN_USERNAME)
            cls.fqdn = fqdn
            cls.tenancy = tenancy

            # Create our test user

            create_tenant_user(cls.USERNAME, cls.PASSWORD, cls.TENANCY_NAME)

    @parameterized.expand(
        [
            ("Normal Looking Tag",),
            ("Füññy Lööking Chàràçtèrß",),
            ("📻📡 🎶",),
        ]
    )
    def test_retrieve_tag(self, name: str):
        """
        Tests we can retrieve a tag through the API.
        """

        # Arrange

        with tenant_context(self.tenancy):
            tag = Tag(tag=name)
            tag.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("tag-detail", kwargs={"pk": tag.id})

        # Act

        response = self.client.get(url, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["tag"], name)

    @parameterized.expand(
        [
            ("Tag 1",),
            ("Tag-2",),
            ("Tag?3",),
        ]
    )
    def test_create_tag_post(self, name: str):
        """
        Tests we can create tags.
        """

        # Arrange

        tag_request = {"tag": name}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("tag-list")

        # Act

        response = self.client.post(url, tag_request, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_response = json.loads(response.content)

        self.assertIsNotNone(json_response["id"])
        self.assertEqual(json_response["tag"], name)

    @parameterized.expand(
        [
            ("Tag 4", "Tag 5"),
            ("Tag-6", "Tag-7"),
            ("Tag?8", "Tag?9"),
        ]
    )
    def test_update_tag(self, original_name: str, new_name: str):
        """
        Tests we can update tags.
        """

        # Arrange

        with tenant_context(self.tenancy):
            tag = Tag(tag=original_name)
            tag.save()

        tag_request = {"tag": new_name}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("tag-detail", kwargs={"pk": tag.id})

        # Act

        response = self.client.put(url, tag_request, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["id"], str(tag.id))
        self.assertEqual(json_response["tag"], new_name)

    def test_delete_tag(self):
        """
        Tests we can delete a tag.
        """

        # Arrange

        with tenant_context(self.tenancy):
            tag = Tag(tag="Tag to Delete")
            tag.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("tag-detail", kwargs={"pk": tag.id})

        # Act

        response = self.client.delete(url, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_rename_collision(self):
        """
        Tests we catch re-name collisions.
        """

        # Arrange

        with tenant_context(self.tenancy):
            tag = Tag(tag="Colliding Tag 1")
            tag.save()
            colliding_tag = Tag(tag="Colliding Tag 2")
            colliding_tag.save()

        tag_request = {"tag": "Colliding Tag 1"}
        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("tag-detail", kwargs={"pk": colliding_tag.id})

        # Act

        response = self.client.put(url, tag_request, **{"HTTP_HOST": self.fqdn})
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["tag"], ["tag with this tag already exists."])

    def test_fail_name_collision(self):
        """
        Tests we can't create a new tag to collide.
        """

        # Arrange

        with tenant_context(self.tenancy):
            tag = Tag(tag="Colliding Tag 1")
            tag.save()

        tag_request = {"tag": "Colliding Tag 1"}
        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("tag-list")

        # Act

        response = self.client.post(url, tag_request, **{"HTTP_HOST": self.fqdn})
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["tag"], ["tag with this tag already exists."])
