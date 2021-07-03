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

from alldaydj.models import Type
from alldaydj.test.utils import set_bearer_token
from django.contrib.auth.models import User
from django.urls import reverse
import json
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from typing import List


class TypeTests(APITestCase):
    """
    Test cases for the type management API.
    """

    ADMIN_USERNAME = "admin@example.com"
    ADMIN_PASSWORD = "1337h@x0r"
    USERNAME = "type@example.com"
    PASSWORD = "$up3rS3cur3"

    @classmethod
    def setUpClass(cls):

        super(TypeTests, cls).setUpClass()

        # Create our test user

        User.objects.create_user(username=cls.USERNAME, password=cls.PASSWORD)

    @parameterized.expand(
        [
            ("Normal Looking Type", "#FF0000", False),
            ("Füññy Lööking Chàràçtèrß", "#00FF00", True),
            ("📻📡 🎶", "#0000FF", False),
        ]
    )
    def test_retrieve_type(self, name: str, colour: str, now_playing: bool):
        """
        Tests we can retrieve a type through the API.
        """

        # Arrange

        cart_type = Type(name=name, colour=colour, now_playing=now_playing)
        cart_type.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("type-detail", kwargs={"pk": cart_type.id})

        # Act

        response = self.client.get(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["name"], name)
        self.assertEqual(json_response["colour"], colour)
        self.assertEqual(json_response["now_playing"], now_playing)

    @parameterized.expand(
        [
            ("Type 1", "#FF0000", False),
            ("Type-2", "#00FF00", True),
            ("Type?3", "#0000FF", False),
        ]
    )
    def test_create_type_post(self, name: str, colour: str, now_playing: bool):
        """
        Tests we can create type.
        """

        # Arrange

        type_request = {"name": name, "colour": colour, "now_playing": now_playing}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("type-list")

        # Act

        response = self.client.post(
            url,
            type_request,
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_response = json.loads(response.content)

        self.assertIsNotNone(json_response["id"])
        self.assertEqual(json_response["name"], name)
        self.assertEqual(json_response["colour"], colour)
        self.assertEqual(json_response["now_playing"], now_playing)

    @parameterized.expand(
        [
            ("Type 4", "Type 5", "#FF0000", False),
            ("Type-6", "Type-7", "#00FF00", True),
            ("Type?8", "Type?9", "#0000FF", False),
        ]
    )
    def test_update_type(
        self, original_name: str, new_name: str, colour: str, now_playing: bool
    ):
        """
        Tests we can update types.
        """

        # Arrange

        cart_type = Type(name=original_name, colour=colour, now_playing=now_playing)
        cart_type.save()

        type_request = {"name": new_name, "colour": colour, "now_playing": now_playing}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("type-detail", kwargs={"pk": cart_type.id})

        # Act

        response = self.client.put(
            url,
            type_request,
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["id"], str(cart_type.id))
        self.assertEqual(json_response["name"], new_name)
        self.assertEqual(json_response["colour"], colour)
        self.assertEqual(json_response["now_playing"], now_playing)

    def test_delete_type(self):
        """
        Tests we can delete a type.
        """

        # Arrange

        cart_type = Type(name="Type to Delete", colour="#C0C0C0", now_playing=False)
        cart_type.save()

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("type-detail", kwargs={"pk": cart_type.id})

        # Act

        response = self.client.delete(
            url,
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_rename_collision(self):
        """
        Tests we catch re-name collisions.
        """

        # Arrange

        cart_type = Type(name="Colliding Type 1", colour="#C0C0C0", now_playing=False)
        cart_type.save()
        colliding_type = Type(
            name="Colliding Type 2", colour="#C0C0C0", now_playing=False
        )
        colliding_type.save()

        type_request = {
            "name": "Colliding Type 1",
            "colour": "#C0C0C0",
            "now_playing": False,
        }
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("type-detail", kwargs={"pk": colliding_type.id})

        # Act

        response = self.client.put(
            url,
            type_request,
        )
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["name"], ["type with this name already exists."])

    def test_fail_name_collision(self):
        """
        Tests we can't create a new type to collide.
        """

        # Arrange

        cart_type = Type(name="Colliding Type 1", colour="#C0C0C0", now_playing=False)
        cart_type.save()

        type_request = {
            "name": "Colliding Type 1",
            "colour": "#C0C0C0",
            "now_playing": False,
        }
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("type-list")

        # Act

        response = self.client.post(
            url,
            type_request,
        )
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["name"], ["type with this name already exists."])
