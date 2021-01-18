"""
    Serializers for AllDay DJ Tenants.
"""

from rest_framework import serializers
from alldaydj.tenants.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    """
    Serializes tenancies.
    """

    class Meta:
        model = Tenant
        fields = ("name", "slug")
