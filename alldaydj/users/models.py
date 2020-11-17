"""
    AllDay DJ User Models
"""

from django.db import models
from django.utils.translation import gettext as _
from tenant_users import UserProfile


class TenantUser(UserProfile):
    """
    User associated with a tenant.
    """

    name = models.CharField(_("Name"), max_length=100, blank=True)