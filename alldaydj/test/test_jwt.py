from alldaydj.test.test_0000_init_tenancies import SetupTests
from alldaydj.test.utils import (
    create_tenancy,
    create_tenant_user,
    set_bearer_token,
)
from django.urls import reverse
from django_tenants.utils import tenant_context
import json
from os import environ
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase
from tenant_users.tenants.tasks import provision_tenant
from typing import List


class JwtAuthTests(APITestCase):
    """
    Tests for JWT authentication.
    """

    STANDARD_USERNAME = "standard@example.com"
    STANDARD_PASSWORD = "$up3rS3cur3"
    TENANT_NAME = "test"
    OTHER_TENANT_NAME = "other"
    PUBLIC_TENANT_NAME = "public"
    PUBLIC_FQDN = f"public.{environ.get('ADDJ_USERS_DOMAIN')}"
    TENANT_FQDN = f"{TENANT_NAME}.{environ.get('ADDJ_USERS_DOMAIN')}"

    @classmethod
    def setUpClass(cls):

        super(JwtAuthTests, cls).setUpClass()

        # Create the tenancies we need

        with tenant_context(SetupTests.PUBLIC_TENANT):
            (cls.standard_fqdn, _) = create_tenancy(
                cls.TENANT_NAME, SetupTests.ADMIN_USERNAME
            )
            (cls.other_fqdn, _) = create_tenancy(
                cls.OTHER_TENANT_NAME, SetupTests.ADMIN_USERNAME
            )

            # And also a standard user

            create_tenant_user(
                cls.STANDARD_USERNAME, cls.STANDARD_PASSWORD, cls.TENANT_NAME
            )

    @parameterized.expand(
        [
            (STANDARD_USERNAME, STANDARD_PASSWORD, TENANT_NAME),
            (SetupTests.ADMIN_USERNAME, SetupTests.ADMIN_PASSWORD, TENANT_NAME),
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

    @parameterized.expand(
        [
            ("bad@example.com", "credsgohere", TENANT_NAME),
            (STANDARD_USERNAME, SetupTests.ADMIN_PASSWORD, TENANT_NAME),
            (SetupTests.ADMIN_USERNAME, STANDARD_PASSWORD, TENANT_NAME),
        ]
    )
    def test_bad_creds(self, username: str, password: str, tenant_name: str):
        """Tests users cannot login with bad credentials.

        Args:
            username (str): The username to try.
            password (str): The password to try.
            tenant_name (str): The tenancy to try logging in on.
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

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @parameterized.expand(
        [
            (STANDARD_USERNAME, STANDARD_PASSWORD, ["test"]),
            (SetupTests.ADMIN_USERNAME, SetupTests.ADMIN_PASSWORD, ["test", "other"]),
        ]
    )
    def test_get_tenancy_list(
        self, username: str, password: str, expected_tenancies: List[str]
    ):
        """
        Checks we get the correct tenancy back for a user.

        Args:
            username (str): The username to test with.
            password (str): The password to test with.
            expected_tenancies (List[str]): The expected list of tenancies.
        """

        # Arrange

        set_bearer_token(username, password, self.PUBLIC_FQDN, self.client)
        url = reverse("tenancies")

        # Act

        response = self.client.get(url, **{"HTTP_HOST": self.PUBLIC_FQDN})

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)
        tenancies = [tenancy["slug"] for tenancy in json_response]

        self.assertEqual(tenancies, expected_tenancies)

    def test_cannot_cross_tenancy(self):
        """
        Tests we can't cross users between tenancies.
        """

        #  Arrange

        url = reverse("tenancies")
        host = f"{self.OTHER_TENANT_NAME}.{environ.get('ADDJ_USERS_DOMAIN')}"

        # Act

        response = self.client.get(url, format="json", **{"HTTP_HOST": host})

        #  Assert

        self.assertEqual(response.status_code, 401)
