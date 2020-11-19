"""
    Models or AllDay DJ Tenants
"""

from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase


class Tenant(TenantBase):
    """
    Tenant of the AllDay DJ web app.
    """

    name = models.TextField()
    auto_create_schema = True

    def __str__(self) -> str:
        return self.name


class Domain(DomainMixin):
    """
    The domain a tenant is associated with.
    """

    pass
