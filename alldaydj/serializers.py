"""
    Serializers for AllDay DJ.
"""

from rest_framework import serializers
from alldaydj.models import Artist, AudioUploadJob, Cart, Tag, Type


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
            "cue_intro_start",
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
