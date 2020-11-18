from alldaydj.models import Artist, Cart, Tag, Type
from alldaydj.tenants.models import Tenant
from alldaydj.test.utils import get_bearer_token, create_tenancy
from django.urls import reverse
from django.conf import settings
from django_tenants.utils import tenant_context
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from typing import List


class CartTests(APITestCase):
    """
    Test cases for the cart management API.
    """

    USERNAME = "cart@example.com"
    PASSWORD = "$up3rS3cur3"
    TENANCY_NAME = "test"

    artists: List[Artist] = []
    tags: List[Tag] = []
    types: List[Type] = []

    @classmethod
    def setUpClass(cls):

        super(CartTests, cls).setUpClass()

        # Create the tenancy

        (fqdn, tenancy) = create_tenancy(
            cls.TENANCY_NAME,
            cls.USERNAME,
            cls.PASSWORD,
            settings.ADDJ_DEFAULT_PERMISSIONS,
        )
        cls.fqdn = fqdn

        # Create some test data

        with tenant_context(tenancy):
            for i in range(3):
                artist = Artist(name=f"Artist {i}")
                tag = Tag(tag=f"Tag {i}")
                type = Type(name=f"Type {i}")

                artist.save()
                tag.save()
                type.save()

                cls.artists.append(artist)
                cls.tags.append(tag)
                cls.types.append(type)

    def test_retrieve_song(self):
        """
        Tere's we can successfully retrieve a song from the API.
        """

        pass