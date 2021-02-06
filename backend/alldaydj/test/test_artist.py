from alldaydj.models import Artist
from alldaydj.test.utils import set_bearer_token
from django.contrib.auth.models import User
from django.urls import reverse
import json
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from typing import List


class ArtistTests(APITestCase):
    """
    Test cases for the artist management API.
    """

    USERNAME = "artist@example.com"
    PASSWORD = "$up3rS3cur3"

    @classmethod
    def setUpClass(cls):

        super(ArtistTests, cls).setUpClass()
        User.objects.create_user(username=cls.USERNAME, password=cls.PASSWORD)

    @parameterized.expand(
        [
            ("Normal Looking Artist",),
            ("Füññy Lööking Chàràçtèrß",),
            ("📻📡 🎶",),
        ]
    )
    def test_retrieve_artist(self, name: str):
        """
        Tests we can retrieve an artist through the API.
        """

        # Arrange

        artist = Artist(name=name)
        artist.save()
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("artist-detail", kwargs={"pk": artist.id})

        # Act

        response = self.client.get(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["name"], name)

    @parameterized.expand(
        [
            ("Artist 1",),
            ("Artist-2",),
            ("Artist?3",),
        ]
    )
    def test_create_artist_post(self, name: str):
        """
        Tests we can create artists.
        """

        # Arrange

        artist_request = {"name": name}
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("artist-list")

        # Act

        response = self.client.post(url, artist_request)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_response = json.loads(response.content)

        self.assertIsNotNone(json_response["id"])
        self.assertEqual(json_response["name"], name)

    @parameterized.expand(
        [
            ("Artist 4", "Artist 5"),
            ("Artist-6", "Artist-7"),
            ("Artist?8", "Artist?9"),
        ]
    )
    def test_update_artist(self, original_name: str, new_name: str):
        """
        Tests we can update artists.
        """

        # Arrange

        artist = Artist(name=original_name)
        artist.save()
        artist_request = {"name": new_name}

        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("artist-detail", kwargs={"pk": artist.id})

        # Act

        response = self.client.put(url, artist_request)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)

        self.assertEqual(json_response["id"], str(artist.id))
        self.assertEqual(json_response["name"], new_name)

    def test_delete_artist(self):
        """
        Tests we can delete an artist.
        """

        # Arrange

        artist = Artist(name="Artist to Delete")
        artist.save()
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("artist-detail", kwargs={"pk": artist.id})

        # Act

        response = self.client.delete(url)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_rename_collision(self):
        """
        Tests we catch re-name collisions.
        """

        # Arrange

        artist = Artist(name="Colliding Artist 1")
        artist.save()
        colliding_artist = Artist(name="Colliding Artist 2")
        colliding_artist.save()

        artist_request = {"name": "Colliding Artist 1"}
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("artist-detail", kwargs={"pk": colliding_artist.id})

        # Act

        response = self.client.put(url, artist_request)
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["name"], ["artist with this name already exists."]
        )

    def test_fail_name_collision(self):
        """
        Tests we can't create a new artist to collide.
        """

        # Arrange

        artist = Artist(name="Colliding Artist 1")
        artist.save()

        artist_request = {"name": "Colliding Artist 1"}
        set_bearer_token(self.USERNAME, self.PASSWORD, self.client)
        url = reverse("artist-list")

        # Act

        response = self.client.post(url, artist_request)
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["name"], ["artist with this name already exists."]
        )
