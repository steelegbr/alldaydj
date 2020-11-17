from django.urls import reverse
import json
from os import environ
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.tasks import provision_tenant
from alldaydj.users.models import TenantUser
from alldaydj.tenants.models import Tenant


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

    @classmethod
    def setUpClass(cls):

        super(JwtAuthTests, cls).setUpClass()

        # Order is important here
        # First create the tenancies

        create_public_tenant(cls.PUBLIC_FQDN, cls.ADMIN_USERNAME)
        cls.standard_fqdn = provision_tenant(
            cls.TENANT_NAME, cls.TENANT_NAME, cls.ADMIN_USERNAME
        )

        # We update the dyanmically create admin user

        cls.admin_user = TenantUser.objects.filter(email=cls.ADMIN_USERNAME).first()
        cls.admin_user.set_password(cls.ADMIN_PASSWORD)
        cls.admin_user.save()

        # And finally a standard user

        cls.standard_user = TenantUser.objects.create_user(
            email=cls.STANDARD_USERNAME,
            password=cls.STANDARD_PASSWORD,
            is_active=True,
        )

        Tenant.objects.filter(name=cls.TENANT_NAME).first().add_user(cls.standard_user)

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
        auth_request = {"email": username, "password": password}
        host = f"{tenant_name}.{environ.get('ADDJ_USERS_DOMAIN')}"

        # Act

        response = self.client.post(
            url, auth_request, format="json", **{"HTTP_HOST": host}
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

        response_json = json.loads(response.content)

        self.assertIsNotNone(response_json)
        self.assertIn("access", response_json)
        self.assertIn("refresh", response_json)
        self.assertIsNotNone(response_json["access"])
        self.assertIsNotNone(response_json["refresh"])

    @parameterized.expand([
        ("bad@example.com", "credsgohere", TENANT_NAME),
        (STANDARD_USERNAME, ADMIN_PASSWORD, TENANT_NAME),
        (ADMIN_USERNAME, STANDARD_PASSWORD, TENANT_NAME),
    ])
    def test_bad_creds(self, username: str, password: str, tenant_name: str):
        """
        Tests users cannot login with bad credentials.
        """

        # Arrange

        url = reverse("token_obtain_pair")
        auth_request = {
            "email": username,
            "password": password,
        }
        host = f"{tenant_name}.{environ.get('ADDJ_USERS_DOMAIN')}"

        # Act

        response = self.client.post(
            url, auth_request, format="json", **{"HTTP_HOST": host}
        )

        #  Assert

        self.assertEqual(response.status_code, 401)
