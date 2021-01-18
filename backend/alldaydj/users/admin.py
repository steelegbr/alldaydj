"""
    AllDay DJ Tenant Admin
"""

from django.contrib import admin
from alldaydj.users.models import TenantUser


@admin.register(TenantUser)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("email",)
