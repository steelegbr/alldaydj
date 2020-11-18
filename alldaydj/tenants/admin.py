"""
    AllDay DJ Tenant Admin
"""

from alldaydj.tenants.models import Tenant
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from tenant_users.tenants.models import UserTenantPermissions

@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name",)

@admin.register(UserTenantPermissions)
class UserTenantPermissionsAdmin(admin.ModelAdmin):
    list_display = ("profile",)
