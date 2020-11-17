from django.urls import reverse
import json
from os import environ
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.tasks import provision_tenant
from alldaydj.users.models import TenantUser


class JwtAuthTests(APITestCase):
    """
    Tests for JWT authentication.
    """

    STANDARD_USERNAME = "standard@example.com"
    STANDARD_PASSWORD = "$up3rS3cur3"
    ADMIN_USERNAME = "admin@example.com"
    ADMIN_PASSWORD = "1337h@x0r"
    TENANT_NAME = "test"
    PUBLIC_TENANT_NAME = "public"
    PUBLIC_FQDN = environ.get("ADDJ_USERS_DOMAIN")
    TENANT_FQDN = f"{TENANT_NAME}.{environ.get('ADDJ_USERS_DOMAIN')}"

    def setUp(self):
        self.standard_user = TenantUser.objects.create_user(
            email=self.STANDARD_USERNAME,
            password=self.STANDARD_PASSWORD,
            is_active=True,
        )
        self.admin_user = TenantUser.objects.create_superuser(
            email=self.ADMIN_USERNAME,
            password=self.ADMIN_PASSWORD,
            is_active=True,
        )

        create_public_tenant(self.PUBLIC_FQDN, self.ADMIN_USERNAME)
        self.standard_fqdn = provision_tenant(self.TENANT_NAME, self.ADMIN_USERNAME)

        

    @parameterized.expand(
        [
            (STANDARD_USERNAME, STANDARD_PASSWORD, TENANT_NAME),
            (ADMIN_USERNAME, ADMIN_PASSWORD, TENANT_NAME),
        ]
    )
    def test_can_authenticate(self, username: str, password: str, tenant_name: str):
        """
        Tests we can authenticate as a specified user.

        Args:
            username (str): The username to test.
            password (str): The password to test.
            tenant_name (str): The name of the tenancy.
        """

        # Arrange

        url = reverse("token_obtain_pair")
        auth_request = {username: username, password: password}

        # Act

        response = self.client.post(
            url, auth_request, format="json", **{"HTTP_HOST", self.TENANT_FQDN}
        )
        response_json = json.loads(response.content)

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_json)
        self.assertIn("access", response_json)
        self.assertIn("refresh", response_json)
        self.assertIsNotNone(response_json.access)
        self.assertIsNotNone(response_json.refresh)
