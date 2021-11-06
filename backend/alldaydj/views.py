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

from django.http.response import JsonResponse
from alldaydj.documents.backends import MatchPhraseFilterBackend
from alldaydj.documents.cart import CartDocument
from alldaydj.models import Artist, AudioUploadJob, Cart, CartIdSequencer, Tag, Type
from alldaydj.serializers import (
    ArtistSerializer,
    AudioSerlializer,
    AudioUploadJobSerializer,
    CartIdSequencerSerialiser,
    CartSerializer,
    CartDocumentSerializer,
    TagSerializer,
    TypeSerializer,
)
from alldaydj.tasks import validate_audio_upload
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import QueryFriendlyPageNumberPagination
import re
from rest_framework.parsers import MultiPartParser
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AudioUploadJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AudioUploadJob.objects.all()
    serializer_class = AudioUploadJobSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartByLabelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = "label"
    lookup_value_regex = "[A-Z0-9]+"


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class AudioView(views.APIView):
    parser_classes = [MultiPartParser]
    queryset = Cart.objects.all()

    @staticmethod
    def post(request, pk):

        # Check we have a cart to match on

        cart = get_object_or_404(Cart, id=pk)

        # Check we have a file uploaded to us

        if "file" not in request.data or not request.data["file"]:
            return HttpResponseBadRequest(
                _("You must upload an audio file to process.")
            )

        # Create the job

        job = AudioUploadJob(cart=cart)
        job.save()

        # Save the file to the queue folder and trigger the process

        generated_file_name = f"queued/{job.id}_{cart.id}"
        default_storage.save(generated_file_name, request.data["file"])
        validate_audio_upload.apply_async(args=(job.id,))

        # Let the user know we're in progress

        job_serial = AudioUploadJobSerializer(job)
        return Response(job_serial.data)

    @staticmethod
    def get(request, pk):

        # Check we have a cart to match on

        cart = get_object_or_404(Cart, id=pk)
        cart_serial = AudioSerlializer(cart)
        return Response(cart_serial.data)


class CartDocumentView(BaseDocumentViewSet):
    document = CartDocument
    serializer_class = CartDocumentSerializer
    pagination_class = QueryFriendlyPageNumberPagination
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        MatchPhraseFilterBackend,
    ]
    search_fields = ["label", "artist", "title"]
    filter_fields = {
        "label": "label.raw",
        "title": "title.raw",
        "artist": "artist.raw",
        "year": {
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ]
        },
    }
    ordering_fields = {
        "_score": "_score",
        "label": "label.raw",
        "artist": "artist.raw",
        "title": "title.raw",
    }
    ordering = (
        "_score",
        "label",
        "artist",
        "title",
    )


class CartIdSequencerViewSet(viewsets.ModelViewSet):
    queryset = CartIdSequencer.objects.all()
    serializer_class = CartIdSequencerSerialiser

    @action(detail=True, methods=["get"])
    def generate_next(self, request, pk=None):
        generator = self.get_object()
        search_regex = (
            f"{generator.prefix}(\\d{{{generator.min_digits},}}){generator.suffix}"
        )
        existing = Cart.objects.filter(label__regex=search_regex).order_by("label")

        next_expected = 1
        for current in existing:
            current_number = int(re.findall(search_regex, current.label)[0])
            if current_number == next_expected:
                next_expected += 1
            else:
                break

        next_padded = str(next_expected).rjust(generator.min_digits, "0")
        return JsonResponse(
            {"next": f"{generator.prefix}{next_padded}{generator.suffix}"}
        )
