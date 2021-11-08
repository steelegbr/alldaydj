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
from alldaydj.models import Artist, AudioUploadJob, Cart, CartIdSequencer, Tag, Type
from alldaydj.serializers import (
    ArtistSerializer,
    AudioSerlializer,
    AudioUploadJobSerializer,
    CartIdSequencerSerialiser,
    CartSerializer,
    TagSerializer,
    TypeSerializer,
)
from alldaydj.tasks import validate_audio_upload
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
import logging
import re
from rest_framework.parsers import MultiPartParser
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().order_by("name")
    serializer_class = ArtistSerializer


class AudioUploadJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AudioUploadJob.objects.all().order_by("id")
    serializer_class = AudioUploadJobSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("label")
    serializer_class = CartSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["label", "title", "display_artist", "year"]
    ordering_fields = ["label", "title", "display_artist"]


class CartByLabelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all().order_by("label")
    serializer_class = CartSerializer
    lookup_field = "label"
    lookup_value_regex = "[A-Z0-9]+"


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("tag")
    serializer_class = TagSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all().order_by("name")
    serializer_class = TypeSerializer


class AudioView(views.APIView):
    parser_classes = [MultiPartParser]
    queryset = Cart.objects.all()

    @staticmethod
    def post(request, pk):

        # Check we have a cart to match on

        cart = get_object_or_404(Cart, id=pk)
        logger.info(f"Found cart {cart.id}")

        # Check we have a file uploaded to us

        if "file" not in request.data or not request.data["file"]:
            logger.warning(f"Update cart {cart.id} audio without audio payload")
            return HttpResponseBadRequest(
                _("You must upload an audio file to process.")
            )

        # Create the job

        job = AudioUploadJob(cart=cart)
        job.save()
        logger.info(f"Created job {job.id} for cart {cart.id}")

        # Save the file to the queue folder and trigger the process

        generated_file_name = f"queued/{job.id}_{cart.id}"
        logger.info(f"Starting upload to {generated_file_name}")
        default_storage.save(generated_file_name, request.data["file"])
        logger.info(f"Completed upload to {generated_file_name}")

        validate_audio_upload.apply_async(args=(job.id,))
        logger.info(f"Async job {job.id} triggered")

        # Let the user know we're in progress

        job_serial = AudioUploadJobSerializer(job)
        return Response(job_serial.data)

    @staticmethod
    def get(request, pk):

        # Check we have a cart to match on

        cart = get_object_or_404(Cart, id=pk)
        cart_serial = AudioSerlializer(cart)
        return Response(cart_serial.data)


class CartIdSequencerViewSet(viewsets.ModelViewSet):
    queryset = CartIdSequencer.objects.all().order_by("name")
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
        complete_generated = f"{generator.prefix}{next_padded}{generator.suffix}"
        logger.info(f"Generator {generator.name} picked complete_generated")
        return JsonResponse({"next": complete_generated})
