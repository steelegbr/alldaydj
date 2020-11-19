"""
    Views for AllDay DJ.
"""

from rest_framework import viewsets
from alldaydj.models import Artist, Cart, Tag, Type
from alldaydj.serializers import (
    ArtistSerializer,
    CartSerializer,
    TagSerializer,
    TypeSerializer,
)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
