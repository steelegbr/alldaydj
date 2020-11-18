"""
    AllDay DJ Tenant Admin
"""

from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from tenant_users.tenants.models import UserTenantPermissions


@admin.register(UserTenantPermissions)
class UserTenantPermissionsAdmin(admin.ModelAdmin):
    list_display = ("profile",)
