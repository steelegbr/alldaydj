"""
    AllDay DJ URL Routing
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("api/admin/", admin.site.urls),
]
