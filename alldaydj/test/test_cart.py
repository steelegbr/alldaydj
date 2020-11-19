from alldaydj.models import Artist, Cart, Tag, Type
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


class CartTests(APITestCase):
    """
    Test cases for the cart management API.
    """

    ADMIN_USERNAME = "admin@example.com"
    ADMIN_PASSWORD = "1337h@x0r"
    USERNAME = "cart@example.com"
    PASSWORD = "$up3rS3cur3"
    TENANCY_NAME = "cart"

    artists: List[Artist] = []
    tags: List[Tag] = []
    types: List[Type] = []

    @classmethod
    def setUpClass(cls):

        super(CartTests, cls).setUpClass()

        # Create the tenancy

        with tenant_context(SetupTests.PUBLIC_TENANT):
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

    @parameterized.expand(
        [
            (
                "CART3",
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
                "CART4",
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
    def test_create_cart_post(
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
        Tests we can successfully post a new cart to the API.
        """

        # Arrange

        cart_request = {
            "label": label,
            "title": title,
            "display_artist": display_artist,
            "artists": artists,
            "cue_audio_start": 0,
            "cue_audio_end": 233040,
            "cue_intro_start": 0,
            "cue_intro_end": 29350,
            "cue_segue": 22606,
            "sweeper": sweeper,
            "year": year,
            "tags": tags,
            "type": type,
        }

        if isrc:
            cart_request["isrc"] = isrc
        if composer:
            cart_request["composer"] = composer
        if publisher:
            cart_request["publisher"] = publisher
        if record_label:
            cart_request["record_label"] = record_label

        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)
        url = reverse("cart-list")

        # Act

        response = self.client.post(url, cart_request, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_response = json.loads(response.content)

        self.assertIsNotNone(json_response["id"])
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

    def test_update_cart(self):
        """
        Tests we can update a cart through a PUT command.
        """

        # Arrange

        with tenant_context(self.tenancy):
            cart = Cart(
                label="CART5",
                title="More Audio Variety",
                display_artist="Artist 1",
                cue_audio_start=0,
                cue_audio_end=233040,
                cue_intro_start=0,
                cue_intro_end=29350,
                cue_segue=22606,
                sweeper=False,
                year=800,
                isrc="ABC123",
                composer="Some Person",
                publisher="Evil Bandits",
                record_label="Money Makers",
                type=Type.objects.get(name="Type 1"),
            )
            cart.artists.set([Artist.objects.get(name="Artist 1")])
            cart.tags.set([Tag.objects.get(tag="Tag 1")])
            cart.save()

        cart_request = {
            "label": "CART6",
            "title": "Updated Audio",
            "display_artist": "Artist 1 & Friends",
            "artists": ["Artist 1"],
            "cue_audio_start": 0,
            "cue_audio_end": 233040,
            "cue_intro_start": 0,
            "cue_intro_end": 29350,
            "cue_segue": 22606,
            "sweeper": True,
            "year": 1999,
            "tags": ["Tag 2"],
            "type": ["Type 2"],
            "isrc": "DEF456",
            "composer": "Tone Deaf",
            "publisher": "Pontificating Publishers",
            "record_label": "Dolla Dolla Bill Y'all",
        }

        url = reverse("cart-detail", kwargs={"pk": cart.id})
        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)

        # Act

        response = self.client.put(url, cart_request, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertIsNotNone(json_response["id"])
        self.assertEqual(json_response["label"], "CART6")
        self.assertEqual(json_response["title"], "Updated Audio")
        self.assertEqual(json_response["display_artist"], "Artist 1 & Friends")
        self.assertEqual(json_response["artists"], ["Artist 1"])
        self.assertEqual(json_response["cue_audio_start"], 0)
        self.assertEqual(json_response["cue_audio_end"], 233040)
        self.assertEqual(json_response["cue_intro_start"], 0)
        self.assertEqual(json_response["cue_intro_end"], 29350)
        self.assertEqual(json_response["cue_segue"], 22606)
        self.assertEqual(json_response["sweeper"], True)
        self.assertEqual(json_response["year"], 1999)
        self.assertEqual(json_response["isrc"], "DEF456")
        self.assertEqual(json_response["composer"], "Tone Deaf")
        self.assertEqual(json_response["publisher"], "Pontificating Publishers")
        self.assertEqual(json_response["record_label"], "Dolla Dolla Bill Y'all")
        self.assertEqual(json_response["tags"], ["Tag 2"])
        self.assertEqual(json_response["type"], "Type 2")

    def test_delete_cart(self):
        """
        Tests we can delete a cart.
        """

        # Arrange

        with tenant_context(self.tenancy):
            cart = Cart(
                label="CART7",
                title="More Audio Variety",
                display_artist="Artist 1",
                cue_audio_start=0,
                cue_audio_end=233040,
                cue_intro_start=0,
                cue_intro_end=29350,
                cue_segue=22606,
                sweeper=False,
                year=800,
                isrc="ABC123",
                composer="Some Person",
                publisher="Evil Bandits",
                record_label="Money Makers",
                type=Type.objects.get(name="Type 1"),
            )
            cart.artists.set([Artist.objects.get(name="Artist 1")])
            cart.tags.set([Tag.objects.get(tag="Tag 1")])
            cart.save()

        url = reverse("cart-detail", kwargs={"pk": cart.id})
        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)

        # Act

        response = self.client.delete(url, **{"HTTP_HOST": self.fqdn})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_rename_collision(self):
        """
        Tests we can't re-name a cart to collide.
        """

        with tenant_context(self.tenancy):
            existing_cart = Cart(
                label="CART8",
                title="Cart 8 for Collision",
                display_artist="Artist 1",
                cue_audio_start=0,
                cue_audio_end=233040,
                cue_intro_start=0,
                cue_intro_end=29350,
                cue_segue=22606,
                sweeper=False,
                year=800,
                isrc="ABC123",
                composer="Some Person",
                publisher="Evil Bandits",
                record_label="Money Makers",
                type=Type.objects.get(name="Type 1"),
            )
            existing_cart.artists.set([Artist.objects.get(name="Artist 1")])
            existing_cart.tags.set([Tag.objects.get(tag="Tag 1")])
            existing_cart.save()

            cart = Cart(
                label="CART9",
                title="Cart 9 for Collision",
                display_artist="Artist 1",
                cue_audio_start=0,
                cue_audio_end=233040,
                cue_intro_start=0,
                cue_intro_end=29350,
                cue_segue=22606,
                sweeper=False,
                year=800,
                isrc="ABC123",
                composer="Some Person",
                publisher="Evil Bandits",
                record_label="Money Makers",
                type=Type.objects.get(name="Type 1"),
            )
            cart.artists.set([Artist.objects.get(name="Artist 1")])
            cart.tags.set([Tag.objects.get(tag="Tag 1")])
            cart.save()

        cart_request = {
            "label": "cart8",
            "title": "Attempt to overwrite!",
            "display_artist": "Artist 1 & Friends",
            "artists": ["Artist 1"],
            "cue_audio_start": 0,
            "cue_audio_end": 233040,
            "cue_intro_start": 0,
            "cue_intro_end": 29350,
            "cue_segue": 22606,
            "sweeper": True,
            "year": 1999,
            "tags": ["Tag 2"],
            "type": ["Type 2"],
            "isrc": "DEF456",
            "composer": "Tone Deaf",
            "publisher": "Pontificating Publishers",
            "record_label": "Dolla Dolla Bill Y'all",
        }

        url = reverse("cart-detail", kwargs={"pk": cart.id})
        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)

        # Act

        response = self.client.put(url, cart_request, **{"HTTP_HOST": self.fqdn})
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["label"], ["cart with this label already exists."]
        )

    def test_fail_name_collision(self):
        """
        Tests we can't create a new cart to collide.
        """

        with tenant_context(self.tenancy):
            existing_cart = Cart(
                label="CART10",
                title="Cart 8 for Collision",
                display_artist="Artist 1",
                cue_audio_start=0,
                cue_audio_end=233040,
                cue_intro_start=0,
                cue_intro_end=29350,
                cue_segue=22606,
                sweeper=False,
                year=800,
                isrc="ABC123",
                composer="Some Person",
                publisher="Evil Bandits",
                record_label="Money Makers",
                type=Type.objects.get(name="Type 1"),
            )
            existing_cart.artists.set([Artist.objects.get(name="Artist 1")])
            existing_cart.tags.set([Tag.objects.get(tag="Tag 1")])
            existing_cart.save()

        cart_request = {
            "label": "cart10",
            "title": "Attempt to overwrite!",
            "display_artist": "Artist 1 & Friends",
            "artists": ["Artist 1"],
            "cue_audio_start": 0,
            "cue_audio_end": 233040,
            "cue_intro_start": 0,
            "cue_intro_end": 29350,
            "cue_segue": 22606,
            "sweeper": True,
            "year": 1999,
            "tags": ["Tag 2"],
            "type": ["Type 2"],
            "isrc": "DEF456",
            "composer": "Tone Deaf",
            "publisher": "Pontificating Publishers",
            "record_label": "Dolla Dolla Bill Y'all",
        }

        url = reverse("cart-list")
        set_bearer_token(self.USERNAME, self.PASSWORD, self.fqdn, self.client)

        # Act

        response = self.client.post(url, cart_request, **{"HTTP_HOST": self.fqdn})
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["label"], ["cart with this label already exists."]
        )
