"""
    Models for AllDay DJ
"""

from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    """
    Tenant of the AllDay DJ web app.
    """

    name = models.TextField()
    auto_create_schema = True


class Domain(DomainMixin):
    """
    The domain a tenant is associated with.
    """

    pass
