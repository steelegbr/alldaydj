from alldaydj.views.audio import CartViewSet, GenreViewSet, TagViewSet
from alldaydj.views.settings import get_settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"cart", CartViewSet)
router.register(r"genre", GenreViewSet)
router.register(r"tag", TagViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/settings", get_settings),
    path("api/", include(router.urls)),
]
