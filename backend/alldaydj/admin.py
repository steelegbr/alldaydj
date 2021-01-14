"""
    Admin interface for the AllDay DJ web app.
"""

from alldaydj.models import Artist, Cart, Tag, Type
from django.contrib import admin


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ["label", "display_artist", "title"]
    list_display = ("label", "display_artist", "title")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["tag"]
    list_display = ("tag",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name",)
