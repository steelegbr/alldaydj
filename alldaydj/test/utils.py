"""
    Test utility functions.
"""

from tenant_users.permissions.models import UserTenantPermissions
from alldaydj.tasks import (
    bootstrap,
    create_tenant,
    create_user,
    join_user_tenancy,
    set_tenant_user_permissions,
)
from alldaydj.tenants.models import Tenant
from django.conf import settings
from django.urls import reverse
import json
from os import environ
from rest_framework import status
from rest_framework.test import APIClient
from typing import List, Tuple


def set_bearer_token(
    username: str, password: str, host: str, client: APIClient
) -> None:
    """Attempts to set the current bearer token for a given user.

    Args:
        username (str): The user to log in as.
        password (str): Their password.
        host (str): The hostname to make the request for.
        client (APIClient): The test client to use for login.
    """

    url = reverse("token_obtain_pair")
    auth_request = {"email": username, "password": password}
    response = client.post(url, auth_request, format="json", **{"HTTP_HOST": host})

    if response.status_code == status.HTTP_200_OK:
        json_response = json.loads(response.content)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {json_response['access']}")


def create_public_tenant(username: str, password: str) -> None:
    """
    Creates the public tenancy.

    Args:
        username (str): The username to create it with.
        password (str): The password to create it with.
    """
    bootstrap.apply(args=("public", username, password))


def create_tenancy(
    name: str,
    username: str,
) -> Tuple[str, Tenant]:
    """
    Creates a new tenancy for testing.

    Args:
        name (str): The name of the tenancy.
        username (str): The username (email) to user for the owner.
        password (str): The password to use for the owner.

    Returns:
        str: The FQDN of the tenancy.
        Tenant: The tenancy we created.
    """

    create_tenant.apply(args=(name, username))

    tenant = Tenant.objects.filter(name=name).first()
    return (f"{name}.{environ.get('ADDJ_USERS_DOMAIN')}", tenant)


def create_tenant_user(
    username: str, password: str, tenancy: str, permissions: List[str] = None
) -> None:
    """Creates a user and assigns them to a tenancy.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        tenancy (str): The tenancy to connect them to.
        permissions (List[str]): The permissions to give the user.
    """

    if not permissions:
        permissions = settings.ADDJ_DEFAULT_PERMISSIONS

    create_user.apply(args=(username, password))
    join_user_tenancy.apply(args=(username, tenancy))
    set_tenant_user_permissions.apply(args=(username, tenancy, permissions))
