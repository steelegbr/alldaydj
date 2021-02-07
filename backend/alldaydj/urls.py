"""
    AllDay DJ URL Routing
"""

from alldaydj.views import (
    ArtistViewSet,
    AudioUploadJobViewSet,
    AudioView,
    CartViewSet,
    TagViewSet,
    TypeViewSet,
)
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register("artist", ArtistViewSet)
router.register("cart", CartViewSet)
router.register("job", AudioUploadJobViewSet)
router.register("tag", TagViewSet)
router.register("type", TypeViewSet)

admin.site.site_header = "AllDay DJ Admin"
admin.site.site_title = "AllDay DJ Admin Portal"
admin.site.index_title = "Welcome to the AllDay DJ Admin Portal"

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/audio/<uuid:pk>/", AudioView.as_view(), name="audio"),
    path("api/", include(router.urls)),
]
