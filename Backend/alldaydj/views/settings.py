from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


@api_view()
@permission_classes([AllowAny])
def get_settings(request: Request):
    return Response(
        {
            "auth_audience": settings.AUTH_PASSTHROUGH["AUDIENCE"],
            "auth_domain": settings.AUTH_PASSTHROUGH["DOMAIN"],
            "auth_client_id": settings.AUTH_PASSTHROUGH["CLIENT_ID"],
        }
    )
