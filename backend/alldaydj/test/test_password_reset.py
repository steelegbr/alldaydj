from django.contrib.auth.models import User
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

VALID_USERNAME = "valid@example.com"
INVALID_USERNAME = "invalid@example.com"
ORIGINAL_PASSWORD = "$up3rS3cur3"


class PasswordResetTests(APITestCase):
    """
    Test cases for password resets.
    """

    @classmethod
    def setUpClass(cls):

        super(PasswordResetTests, cls).setUpClass()

        # Create  a standard user

        User.objects.create_user(username=VALID_USERNAME, password=ORIGINAL_PASSWORD)

    @parameterized.expand([(VALID_USERNAME,), (INVALID_USERNAME,)])
    def test_200_response_all_usernames(self, username):
        """
        Ensure no data leak as we return a 200 even if the username is not valid.
        """

        # Arrange

        url = reverse("password_reset:reset-password-request")
        params = {"email": username}

        # Act

        response = self.client.post(url, params)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
