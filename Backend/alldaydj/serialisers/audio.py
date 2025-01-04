from alldaydj.models.audio import Cart, Genre, Tag
from rest_framework.serializers import ModelSerializer


class CartSerialiser(ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class GenreSerialiser(ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TagSerialiser(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
