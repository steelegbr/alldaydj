from types import SimpleNamespace
from alldaydj.signals.handlers import password_reset_token_created
from django.contrib.auth.models import User
from django.core import mail
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

    def test_password_reset_sends_email(self):
        """
        Password reset sends an e-mail
        """

        # Arrange

        dummy_user = User()
        dummy_user.first_name = "Test"
        dummy_user.last_name = "User"
        dummy_user.username = "test01"
        dummy_user.email = "test@alldaydj.net"

        reset_password_token = SimpleNamespace()
        reset_password_token.user = dummy_user
        reset_password_token.username = "test01"
        reset_password_token.email = "test@alldaydj.net"
        reset_password_token.key = "ABC123"

        with open(
            "./alldaydj/test/files/reset_password.txt", "r"
        ) as mail_content_plain_file:
            mail_content_plain = mail_content_plain_file.read()

        with open(
            "./alldaydj/test/files/reset_password_html.txt", "r"
        ) as mail_content_html_file:
            mail_content_html = mail_content_html_file.read()

        # Act

        password_reset_token_created(None, None, reset_password_token, None, None)

        # Assert

        self.assertEqual(len(mail.outbox), 1)
        reset_message = mail.outbox[0]
        self.assertEqual(reset_message.to, ["test@alldaydj.net"])
        self.assertEqual(reset_message.from_email, "noreply@alldaydj.net")
        self.assertEqual(reset_message.subject, "AllDay DJ Password Reset")
        self.assertEqual(reset_message.body, mail_content_plain)

        self.assertEqual(len(reset_message.alternatives), 1)
        html_alternative, type_of_file = reset_message.alternatives[0]
        self.assertEqual(html_alternative, mail_content_html)
        self.assertEqual(type_of_file, "text/html")
