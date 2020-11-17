"""
    Views for AllDay DJ
"""

from alldaydj.tenants.serializers import TenantSerializer
from alldaydj.tenants.models import Tenant
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TenantViewSet(generics.ListAPIView):
    """
    Read-only view into tenants.
    """

    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        tenancies = user.tenants.exclude(name="Public Tenant")
        serializer = TenantSerializer(tenancies, many=True)
        return Response(serializer.data)
