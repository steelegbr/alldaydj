"""
    Test utility functions.
"""

from tenant_users.permissions.models import UserTenantPermissions
from alldaydj.tenants.models import Tenant
from alldaydj.users.models import TenantUser
from django.contrib.auth.models import Permission
from django.urls import reverse
from django_tenants.utils import tenant_context
import json
from os import environ
from rest_framework import status
from rest_framework.test import APIClient
from tenant_users.tenants.tasks import provision_tenant
from tenant_users.tenants.utils import create_public_tenant
from django_tenants.utils import get_public_schema_name
from typing import List, Tuple


def get_bearer_token(username: str, password: str, host: str, client: APIClient) -> str:
    """Obtains a current bearer token for a given user.

    Args:
        username (str): The user to log in as.
        password (str): Their password.
        host (str): The hostname to make the request for.
        client (APIClient): The test client to use for login.

    Returns:
        str: The bearer token (if we can get it).
    """

    url = reverse("token_obtain_pair")
    auth_request = {"email": username, "password": password}
    response = client.post(url, auth_request, format="json", **{"HTTP_HOST": host})

    if response.status_code == status.HTTP_200_OK:
        json_response = json.loads(response.content)
        return json_response["access"]
    else:
        pass


def create_tenancy(
    name: str, username: str, password: str, permissions: List[str]
) -> Tuple[str, Tenant]:
    """
    Creates a new tenancy for testing.

    Args:
        name (str): The name of the tenancy.
        username (str): The username (email) to user for the owner.
        password (str): The password to use for the owner.
        permissions (List[str]): The list of permissions to give the user.

    Returns:
        str: The FQDN of the tenancy.
        Tenant: The tenancy we created.
    """

    # We need a public tenant to start with

    public_fqdn = f"public.{environ.get('ADDJ_USERS_DOMAIN')}"
    create_public_tenant(public_fqdn, username)

    # Now create the specific tenant

    tenant_fqdn = provision_tenant(name, name, username)

    # Assign permissions

    tenancy = Tenant.objects.filter(name=name).first()
    user = TenantUser.objects.filter(email=username).first()

    with tenant_context(tenancy):
        (user_permissions, _) = UserTenantPermissions.objects.get_or_create(profile=user)

        for permission in permissions:
            current_permission = Permission.objects.get(codename=permission)
            user_permissions.user_permissions.add(current_permission)

        user_permissions.save()

    return tenant_fqdn, tenancy
