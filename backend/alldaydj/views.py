"""
    Views for AllDay DJ.
"""

from alldaydj.models import Artist, AudioUploadJob, Cart, Tag, Type
from alldaydj.serializers import (
    ArtistSerializer,
    AudioSerlializer,
    AudioUploadJobSerializer,
    CartSerializer,
    CartSearchSerializer,
    TagSerializer,
    TypeSerializer,
)
from alldaydj.tasks import validate_audio_upload
from drf_haystack.viewsets import HaystackViewSet
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser
from rest_framework import views
from rest_framework import viewsets
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

        if not "file" in request.data or not request.data["file"]:
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


class CartSearchView(HaystackViewSet):
    index_models = [Cart]
    serializer_class = CartSearchSerializer
