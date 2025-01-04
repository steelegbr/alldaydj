from alldaydj.models import Cart, Genre, Tag
from alldaydj.serialisers.audio import CartSerialiser, GenreSerialiser, TagSerialiser
from rest_framework.viewsets import ModelViewSet


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerialiser


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerialiser


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
