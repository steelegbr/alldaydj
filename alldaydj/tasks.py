"""
    Async tasks for AllDay DJ.
"""

from alldaydj.users.models import TenantUser
from alldaydj.tenants.models import Tenant
from celery import shared_task
from django_tenants.utils import tenant_context
from os import environ
from tenant_users.tenants.tasks import provision_tenant
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.models import UserTenantPermissions
from typing import Any


@shared_task
def bootstrap(
    public_tenancy_name: str, admin_username: str, admin_password: str
) -> str:
    """
    Bootstraps the public tenancy.

    Args:
        public_tenancy_name (str): The name of the public tenancy.
        admin_username (str): The admin username. Must be an e-mail address.
        admin_password (str): The admin password.
    """

    create_public_tenant(
        f"{public_tenancy_name}.{environ.get('ADDJ_USERS_DOMAIN')}", admin_username
    )

    admin_user = TenantUser.objects.filter(email=admin_username)[0]
    admin_user.set_password(admin_password)
    admin_user.save()

    return f"Successfully bootstrapped the {public_tenancy_name} public tenancy with {admin_username}."


@shared_task
def create_tenant(tenant_name: str, username: str) -> str:
    """
    Creates a new tenant.

    Args:
        tenant_name (str): The name / slug for the tenant.
        username (str): The username for the owner.
    """

    provision_tenant(tenant_name, tenant_name, username)
    return f"Successfully created the {tenant_name} tenancy."


@shared_task
def create_user(email: str, password: str) -> str:
    """Create a user.

    Args:
        email (str): The e-mail address.
        password (str): The password.
    """

    user = TenantUser.objects.create_user(email=email, password=password)

    return f"Successfully created the {email} user."


def __set_tenant_permissions(
    user: Any, tenant: Any, superuser: bool, staff: bool
) -> None:
    """Sets the specified user permissions on a tenant.

    Args:
        user (Any): The user to set the permissions for.
        tenant (Any): The tenant to set the permissions on.
        superuser (bool): Indicates if the user should be a superuser.
        staff (bool): Indicates if the user should be staff.
    """
    with tenant_context(tenant):
        UserTenantPermissions.objects.get_or_create(
            profile=user, is_staff=staff, is_superuser=superuser
        )


@shared_task
def make_superuser(email: str, tenant_name: str, staff: bool, superuser: bool) -> str:
    """Makes a user a superuser.

    Args:
        email (str): The e-mail address of the user to upgrade.
        tenant_name (str): Optional - indicates if we should restrict to a specific tenant.
        staff (bool): Indicates if the staff privilege is needed.
        superuser (bool): Indicates if the superuser privilege is needed.
    """

    # Find the user

    user = TenantUser.objects.filter(email=email).first()
    if not user:
        raise ValueError(f"Could not find user {email}.")

    if tenant_name:

        # Specific tenancy

        tenant = Tenant.objects.filter(name=tenant_name).first()
        if not tenant:
            raise ValueError(f"Could not find tenant {tenant_name}.")

        # Set the permissions

        __set_tenant_permissions(user, tenant, staff, superuser)

        return f"Successfully applied permissions for {user} on the {tenant} tenancy."

    else:

        # Every tenancy

        tenants = Tenant.objects.all()
        for tenant in tenants:
            __set_tenant_permissions(user, tenant, staff, superuser)

        return f"Successfully applied permissions for {user} on all tenancies."
