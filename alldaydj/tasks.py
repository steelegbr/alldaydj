"""
    Async tasks for AllDay DJ.
"""

from alldaydj.users.models import TenantUser
from alldaydj.tenants.models import Tenant
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import Permission
from django_tenants.utils import tenant_context
from os import environ
from tenant_users.tenants.tasks import provision_tenant
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.models import ExistsError, UserTenantPermissions
from typing import Any, List


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

    admin_user = TenantUser.objects.filter(email=admin_username).first()
    admin_user.set_password(admin_password)
    admin_user.save()

    # Continue into making the user a god

    make_superuser.apply_async(args=(admin_username, "Public Tenant", True, True))

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
    make_superuser.apply_async(args=(username, tenant_name, True, True))
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

        permission = UserTenantPermissions.objects.get(profile=user)

        if permission:
            permission.is_staff = staff
            permission.is_superuser = superuser
            permission.save()
        else:
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


@shared_task
def set_tenant_user_permissions(
    username: str, tenancy: str, permissions: List[str]
) -> str:
    """
    Sets the permissions for a given user in a specified tenancy.

    Args:
        username (str): The username to set the permissions for.
        tenancy (str): The tenancy to set the permissions on.
        permissions (List[str]): The permissions to set.
    """

    # Find the user

    user = TenantUser.objects.filter(email=username).first()
    if not user:
        raise ValueError(f"Failed to find user {username}.")

    # Find the tenancy

    tenant = Tenant.objects.filter(name=tenancy).first()
    if not tenant:
        raise ValueError(f"Failed to find the {tenancy} tenancy.")

    # Apply the permissions

    with tenant_context(tenant):
        (user_permissions, _) = UserTenantPermissions.objects.get_or_create(profile=user)

        for permission in permissions:
            current_permission = Permission.objects.get(codename=permission)
            user_permissions.user_permissions.add(current_permission)

        user_permissions.save()

    return f"Successfully updated permissions for {username} in {tenancy}."


@shared_task
def join_user_tenancy(username: str, tenancy: str) -> str:
    """
    Joins a specific user to a tenancy with default permissions.

    Args:
        username (str): The user to join.
        tenancy (str): The name of the tenancy.
    """

    # Find the user

    user = TenantUser.objects.filter(email=username).first()
    if not user:
        raise ValueError(f"Failed to find user {username}.")

    # Find the tenancy

    tenant = Tenant.objects.filter(name=tenancy).first()
    if not tenant:
        raise ValueError(f"Failed to find the {tenancy} tenancy.")

    # Make the magic happen

    try:
        tenant.add_user(user)
    except ExistsError:
        # Silently ignore if it's already done
        pass

    # Set the default permissions

    set_tenant_user_permissions.apply_async(
        args=(username, tenancy, settings.ADDJ_DEFAULT_PERMISSIONS)
    )

    return f"Successfully added {username} to the {tenancy} tenancy."
