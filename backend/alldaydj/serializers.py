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

from alldaydj.documents.cart import CartDocument
from alldaydj.models import Artist, AudioUploadJob, Cart, CartIdSequencer, Tag, Type
from django.core.files.storage import default_storage
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            "id",
            "name",
        )


class AudioUploadJobSerializer(serializers.ModelSerializer):
    cart = serializers.SlugRelatedField(slug_field="id", read_only=True)

    class Meta:
        model = AudioUploadJob
        fields = ("id", "status", "cart")


class AudioSerlializer(serializers.ModelSerializer):
    audio = serializers.SerializerMethodField()
    compressed = serializers.SerializerMethodField()

    @staticmethod
    def get_audio(cart):
        return default_storage.url(cart.audio)

    @staticmethod
    def get_compressed(cart):
        return default_storage.url(cart.compressed)

    class Meta:
        model = Cart
        fields = ("audio", "compressed", "hash_audio", "hash_compressed")


class CartSerializer(serializers.ModelSerializer):
    artists = serializers.SlugRelatedField(
        slug_field="name", queryset=Artist.objects.all(), many=True
    )
    tags = serializers.SlugRelatedField(
        slug_field="tag", queryset=Tag.objects.all(), many=True
    )
    type = serializers.SlugRelatedField(slug_field="name", queryset=Type.objects.all())

    class Meta:
        model = Cart
        fields = (
            "label",
            "id",
            "title",
            "display_artist",
            "artists",
            "cue_audio_start",
            "cue_audio_end",
            "cue_intro_end",
            "cue_segue",
            "sweeper",
            "year",
            "isrc",
            "composer",
            "publisher",
            "record_label",
            "tags",
            "type",
            "hash_audio",
            "hash_compressed",
            "fade",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "tag",
        )


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("id", "name", "colour", "now_playing")


class CartDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CartDocument
        fields = (
            "label",
            "id",
            "title",
            "artist",
            "year",
        )


class CartIdSequencerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CartIdSequencer
        fields = ("id", "name", "prefix", "suffix", "min_digits")
