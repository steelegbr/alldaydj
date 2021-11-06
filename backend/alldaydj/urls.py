"""
    AllDay DJ - Radio Automation
    Copyright (C) 2020-2021 Marc Steele

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from alldaydj.views import (
    ArtistViewSet,
    AudioUploadJobViewSet,
    AudioView,
    CartByLabelViewSet,
    CartIdSequencerViewSet,
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
router.register("cart/by-label", CartByLabelViewSet, basename="cart-label")
router.register("cart", CartViewSet)
router.register("job", AudioUploadJobViewSet)
router.register("tag", TagViewSet)
router.register("type", TypeViewSet)
router.register("sequencer", CartIdSequencerViewSet)

admin.site.site_header = "AllDay DJ Admin"
admin.site.site_title = "AllDay DJ Admin Portal"
admin.site.index_title = "Welcome to the AllDay DJ Admin Portal"

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/audio/<uuid:pk>/", AudioView.as_view(), name="audio"),
    path(
        "api/password-reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("api/", include(router.urls)),
]
