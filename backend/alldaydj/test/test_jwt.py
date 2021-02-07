from alldaydj.test.utils import set_bearer_token
from django.contrib.auth.models import User
from django.urls import reverse
import json
from os import environ
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from typing import List


class JwtAuthTests(APITestCase):
    """
    Tests for JWT authentication.
    """

    STANDARD_USERNAME = "standard@example.com"
    STANDARD_PASSWORD = "$up3rS3cur3"

    @classmethod
    def setUpClass(cls):

        super(JwtAuthTests, cls).setUpClass()

        # Create  a standard user

        User.objects.create_user(
            username=cls.STANDARD_USERNAME, password=cls.STANDARD_PASSWORD
        )

    @parameterized.expand(
        [
            (STANDARD_USERNAME, STANDARD_PASSWORD),
        ]
    )
    def test_can_authenticate(self, username: str, password: str):
        """
        Tests we can authenticate as a specified user.

        Args:
            username (str): The username to test.
            password (str): The password to test.
        """

        # Arrange

        url = reverse("token_obtain_pair")
        auth_request = {"username": username, "password": password}

        # Act

        response = self.client.post(url, auth_request, format="json")

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

        response_json = json.loads(response.content)

        self.assertIsNotNone(response_json)
        self.assertIn("access", response_json)
        self.assertIn("refresh", response_json)
        self.assertIsNotNone(response_json["access"])
        self.assertIsNotNone(response_json["refresh"])

    @parameterized.expand(
        [
            ("bad@example.com", "credsgohere"),
        ]
    )
    def test_bad_creds(self, username: str, password: str):
        """Tests users cannot login with bad credentials.

        Args:
            username (str): The username to try.
            password (str): The password to try.
        """

        # Arrange

        url = reverse("token_obtain_pair")
        auth_request = {
            "username": username,
            "password": password,
        }

        # Act

        response = self.client.post(url, auth_request, format="json")

        #  Assert

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
