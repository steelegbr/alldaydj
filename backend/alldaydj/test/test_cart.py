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

from unittest.mock import call, patch
from alldaydj.models import Artist, Cart, Tag, Type
from alldaydj.test.utils import set_bearer_token
from django.contrib.auth.models import User
from django.urls import reverse
import json
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

    artists: List[Artist] = []
    tags: List[Tag] = []
    types: List[Type] = []

    @classmethod
    def setUpClass(cls):

        super(CartTests, cls).setUpClass()

        #  Create our test user

        User.objects.create_user(username=cls.USERNAME, password=cls.PASSWORD)

        # Create some test data

        for i in range(4):
            artist = Artist(name=f"Artist {i}")
            tag = Tag(tag=f"Tag {i}")
            cart_type = Type(name=f"Type {i}")

            artist.save()
            tag.save()
            cart_type.save()

            cls.artists.append(artist)
            cls.tags.append(tag)
            cls.types.append(cart_type)

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
        cart_type: Type,
    ):
        """
        Tere's we can successfully retrieve a song from the API.
        """

        # Arrange

        cart = Cart(
            label=label,
            title=title,
            display_artist=display_artist,
            cue_audio_start=0,
            cue_audio_end=233040,
            cue_intro_end=29350,
            cue_segue=22606,
            sweeper=sweeper,
            year=year,
            isrc=isrc,
            composer=composer,
            publisher=publisher,
            record_label=record_label,
            type=Type.objects.get(name=cart_type),
        )
        cart.artists.set([Artist.objects.get(name=artist) for artist in artists])
        cart.tags.set([Tag.objects.get(tag=tag) for tag in tags])
        cart.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("cart-detail", kwargs={"pk": cart.id})

        # Act

        response = self.client.get(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["label"], label)
        self.assertEqual(json_response["title"], title)
        self.assertEqual(json_response["display_artist"], display_artist)
        self.assertEqual(json_response["artists"], artists)
        self.assertEqual(json_response["cue_audio_start"], 0)
        self.assertEqual(json_response["cue_audio_end"], 233040)
        self.assertEqual(json_response["cue_intro_end"], 29350)
        self.assertEqual(json_response["cue_segue"], 22606)
        self.assertEqual(json_response["sweeper"], sweeper)
        self.assertEqual(json_response["year"], year)
        self.assertEqual(json_response["isrc"], isrc)
        self.assertEqual(json_response["composer"], composer)
        self.assertEqual(json_response["publisher"], publisher)
        self.assertEqual(json_response["record_label"], record_label)
        self.assertEqual(json_response["tags"], tags)
        self.assertEqual(json_response["type"], cart_type)

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
    def test_retrieve_song_by_label(
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
        cart_type: Type,
    ):
        """
        Tere's we can successfully retrieve a song from the API by the label.
        """

        # Arrange

        cart = Cart(
            label=label,
            title=title,
            display_artist=display_artist,
            cue_audio_start=0,
            cue_audio_end=233040,
            cue_intro_end=29350,
            cue_segue=22606,
            sweeper=sweeper,
            year=year,
            isrc=isrc,
            composer=composer,
            publisher=publisher,
            record_label=record_label,
            type=Type.objects.get(name=cart_type),
        )
        cart.artists.set([Artist.objects.get(name=artist) for artist in artists])
        cart.tags.set([Tag.objects.get(tag=tag) for tag in tags])
        cart.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("cart-label-detail", kwargs={"label": cart.label})

        # Act

        response = self.client.get(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["label"], label)
        self.assertEqual(json_response["title"], title)
        self.assertEqual(json_response["display_artist"], display_artist)
        self.assertEqual(json_response["artists"], artists)
        self.assertEqual(json_response["cue_audio_start"], 0)
        self.assertEqual(json_response["cue_audio_end"], 233040)
        self.assertEqual(json_response["cue_intro_end"], 29350)
        self.assertEqual(json_response["cue_segue"], 22606)
        self.assertEqual(json_response["sweeper"], sweeper)
        self.assertEqual(json_response["year"], year)
        self.assertEqual(json_response["isrc"], isrc)
        self.assertEqual(json_response["composer"], composer)
        self.assertEqual(json_response["publisher"], publisher)
        self.assertEqual(json_response["record_label"], record_label)
        self.assertEqual(json_response["tags"], tags)
        self.assertEqual(json_response["type"], cart_type)

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
        cart_type: Type,
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
            "cue_intro_end": 29350,
            "cue_segue": 22606,
            "sweeper": sweeper,
            "year": year,
            "tags": tags,
            "type": cart_type,
        }

        if isrc:
            cart_request["isrc"] = isrc
        if composer:
            cart_request["composer"] = composer
        if publisher:
            cart_request["publisher"] = publisher
        if record_label:
            cart_request["record_label"] = record_label

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("cart-list")

        # Act

        response = self.client.post(url, cart_request)

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
        self.assertEqual(json_response["cue_intro_end"], 29350)
        self.assertEqual(json_response["cue_segue"], 22606)
        self.assertEqual(json_response["sweeper"], sweeper)
        self.assertEqual(json_response["year"], year)
        self.assertEqual(json_response["isrc"], isrc)
        self.assertEqual(json_response["composer"], composer)
        self.assertEqual(json_response["publisher"], publisher)
        self.assertEqual(json_response["record_label"], record_label)
        self.assertEqual(json_response["tags"], tags)
        self.assertEqual(json_response["type"], cart_type)

    def test_update_cart(self):
        """
        Tests we can update a cart through a PUT command.
        """

        # Arrange

        cart = Cart(
            label="CART5",
            title="More Audio Variety",
            display_artist="Artist 1",
            cue_audio_start=0,
            cue_audio_end=233040,
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
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)

        # Act

        response = self.client.put(url, cart_request)

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

    @patch("django.core.files.storage.default_storage.exists")
    @patch("django.core.files.storage.default_storage.delete")
    def test_delete_cart(self, delete_mock, exists_mock):
        """
        Tests we can delete a cart.
        """

        # Arrange

        cart = Cart(
            label="CART7",
            title="More Audio Variety",
            display_artist="Artist 1",
            cue_audio_start=0,
            cue_audio_end=233040,
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

        exists_mock.side_effect = [True, False]
        expected_exists_calls = [
            call(f"audio/{cart.id}"),
            call(f"compressed/{cart.id}"),
        ]

        url = reverse("cart-detail", kwargs={"pk": cart.id})
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)

        # Act

        response = self.client.delete(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(exists_mock.call_count, 2)
        exists_mock.assert_has_calls(expected_exists_calls)
        self.assertEqual(delete_mock.call_count, 1)
        delete_mock.assert_called_with(f"audio/{cart.id}")

    def test_fail_rename_collision(self):
        """
        Tests we can't re-name a cart to collide.
        """

        existing_cart = Cart(
            label="CART8",
            title="Cart 8 for Collision",
            display_artist="Artist 1",
            cue_audio_start=0,
            cue_audio_end=233040,
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
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)

        # Act

        response = self.client.put(url, cart_request)
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

        existing_cart = Cart(
            label="CART10",
            title="Cart 8 for Collision",
            display_artist="Artist 1",
            cue_audio_start=0,
            cue_audio_end=233040,
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
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)

        # Act

        response = self.client.post(url, cart_request)
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["label"], ["cart with this label already exists."]
        )
