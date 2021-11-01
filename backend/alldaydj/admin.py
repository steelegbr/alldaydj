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

from alldaydj.models import Artist, Cart, CartIdSequencer, Tag, Type
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


@admin.register(CartIdSequencer)
class CartIdSequencerAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name", "prefix", "min_digits", "suffix")
