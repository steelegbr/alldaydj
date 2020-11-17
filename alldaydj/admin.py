"""
    Admin interface for the AllDay DJ web app.
"""

from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from alldaydj.models import Tenant


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name",)
