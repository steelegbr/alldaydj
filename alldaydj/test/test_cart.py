from alldaydj.models import Artist, Cart, Tag, Type
from alldaydj.tenants.models import Tenant
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


class CartTests(APITestCase):
    """
    Test cases for the cart management API.
    """

    ADMIN_USERNAME = "admin@example.com"
    ADMIN_PASSWORD = "1337h@x0r"
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

        create_public_tenant(cls.ADMIN_USERNAME, cls.ADMIN_PASSWORD)
        (fqdn, tenancy) = create_tenancy(cls.TENANCY_NAME, cls.ADMIN_USERNAME)
        cls.fqdn = fqdn
        cls.tenancy = tenancy

        # Create our test user

        create_tenant_user(cls.USERNAME, cls.PASSWORD, cls.TENANCY_NAME)

        # Create some test data

        with tenant_context(cls.tenancy):
            for i in range(4):
                artist = Artist(name=f"Artist {i}")
                tag = Tag(tag=f"Tag {i}")
                type = Type(name=f"Type {i}")

                artist.save()
                tag.save()
                type.save()

                cls.artists.append(artist)
                cls.tags.append(tag)
                cls.types.append(type)

    @parameterized.expand(
        [
            (
                "CART1",
                "Test Title",
                "Artist 1 & Artist 2",
                ["Artist 1", "Artist 2"],
                False,
                1980,
                "ISRC123",
                "Composer 1",
                "Publisher 1",
                "Label 1 Ltd",
                ["Tag 1", "Tag 2"],
                "Type 1",
            ),
            (
                "CART2",
                "Test Title",
                "Artist 3",
                ["Artist 3"],
                True,
                1880,
                None,
                None,
                None,
                None,
                [],
                "Type 2",
            ),
        ]
    )
    def test_retrieve_song(
        self,
        label: str,
        title: str,
        display_artist: str,
        artists: List[Artist],
        sweeper: bool,
        year: int,
        isrc: str,
        composer: str,
        publisher: str,
        record_label: str,
        tags: List[Tag],
        type: Type,
    ):
        """
        Tere's we can successfully retrieve a song from the API.
        """

        # Arrange

        with tenant_context(self.tenancy):
            cart = Cart(
                label=label,
                title=title,
                display_artist=display_artist,
                cue_audio_start=0,
                cue_audio_end=233040,
                cue_intro_start=0,
                cue_intro_end=29350,
                cue_segue=22606,
                sweeper=sweeper,
                year=year,
                isrc=isrc,
                composer=composer,
                publisher=publisher,
                record_label=record_label,
                type=Type.objects.get(name=type),
            )
            cart.artists.set([Artist.objects.get(name=artist) for artist in artists])
            cart.tags.set([Tag.objects.get(tag=tag) for tag in tags])
            cart.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("cart-detail", kwargs={"pk": cart.id})

        # Act

        response = self.client.get(url, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["label"], label)
        self.assertEqual(json_response["title"], title)
        self.assertEqual(json_response["display_artist"], display_artist)
        self.assertEqual(json_response["artists"], artists)
        self.assertEqual(json_response["cue_audio_start"], 0)
        self.assertEqual(json_response["cue_audio_end"], 233040)
        self.assertEqual(json_response["cue_intro_start"], 0)
        self.assertEqual(json_response["cue_intro_end"], 29350)
        self.assertEqual(json_response["cue_segue"], 22606)
        self.assertEqual(json_response["sweeper"], sweeper)
        self.assertEqual(json_response["year"], year)
        self.assertEqual(json_response["isrc"], isrc)
        self.assertEqual(json_response["composer"], composer)
        self.assertEqual(json_response["publisher"], publisher)
        self.assertEqual(json_response["record_label"], record_label)
        self.assertEqual(json_response["tags"], tags)
        self.assertEqual(json_response["type"], type)
