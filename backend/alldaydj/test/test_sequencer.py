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

import json

from django.contrib.auth.models import User
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from alldaydj.models import Cart, CartIdSequencer, Type
from alldaydj.test.utils import set_bearer_token


class SequencerTest(APITestCase):
    """
    Test cases for the cart ID sequencer
    """

    ADMIN_USERNAME = "admin@example.com"
    ADMIN_PASSWORD = "1337h@x0r"
    USERNAME = "sequencer@example.com"
    PASSWORD = "$up3rS3cur3"

    @classmethod
    def setUpClass(cls):

        super(SequencerTest, cls).setUpClass()

        # Create our test user

        User.objects.create_user(username=cls.USERNAME, password=cls.PASSWORD)

        # And a test cart type

        cls.cart_type = Type(name="Test Type")
        cls.cart_type.save()

    def test_generate_from_empty(self):
        """
        Tests we can generate a sequence from 1.
        """

        sequence = CartIdSequencer()
        sequence.name = "Empty Test"
        sequence.prefix = "EMPTY"
        sequence.min_digits = 5
        sequence.suffix = ""
        sequence.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("cartidsequencer-generate-next", kwargs={"pk": sequence.id})

        # Act

        response = self.client.get(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["next"], "EMPTY00001")

    @parameterized.expand(
        [
            ("Start of Sequence", "START", "", 5, "START00001", "START00002"),
            ("End of Sequence", "START", "END", 3, "START999END", "START1000END"),
        ]
    )
    def test_generate_from_cart(
        self,
        name: str,
        prefix: str,
        suffix: str,
        min_digits: int,
        cart_id: str,
        expected_next: str,
    ):
        """
        Tests we can generate a sequence from a cart.
        """

        sequence = CartIdSequencer()
        sequence.name = name
        sequence.prefix = prefix
        sequence.min_digits = min_digits
        sequence.suffix = suffix
        sequence.save()

        cart = Cart(
            label=cart_id,
            title="Test Cart",
            display_artist="Test Artist",
            cue_audio_start=0,
            cue_audio_end=0,
            cue_intro_end=0,
            cue_segue=0,
            sweeper=False,
            year=2020,
            isrc="ISRC123",
            composer="Composer Name",
            publisher="Publisher Name",
            record_label="Record Label",
            type=self.cart_type,
        )

        cart.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("cartidsequencer-generate-next", kwargs={"pk": sequence.id})

        # Act

        response = self.client.get(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["next"], expected_next)
