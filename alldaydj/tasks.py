"""
    Async tasks for AllDay DJ.
"""

from alldaydj.users.models import TenantUser
from celery import shared_task
from os import environ
from tenant_users.tenants.utils import create_public_tenant


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
