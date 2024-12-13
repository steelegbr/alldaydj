from alldaydj.views.settings import get_settings
from django.contrib import admin
from django.urls import path

urlpatterns = [path("admin/", admin.site.urls), path("api/settings", get_settings)]
