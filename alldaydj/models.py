"""
    Models for AllDay DJ
"""

from colorfield.fields import ColorField
from django.contrib.postgres.fields import CITextField
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Artist(models.Model):
    """
    An artist or group that can be associated with a cart.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CITextField(unique=True, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """
    A scheduler / categorisation tag that can be added to a cart.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = CITextField(unique=True, blank=False, null=False)

    def __str__(self) -> str:
        return self.tag


class Type(models.Model):
    """
    Indicates a cart type (less specific than a scheduler category).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CITextField(unique=True, blank=False, null=False)
    colour = ColorField(default="#AC1AF7")
    now_playing = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
    """
    A cart with audio attached.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = CITextField(
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(r"[a-zA-Z0-9]+")],
    )
    title = models.TextField(blank=False, null=False)
    display_artist = models.TextField()
    artists = models.ManyToManyField(Artist)
    cue_audio_start = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cue_audio_end = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cue_intro_start = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cue_intro_end = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cue_segue = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    sweeper = models.BooleanField(default=False, blank=False, null=False)
    year = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    isrc = models.TextField(null=True)
    composer = models.TextField(null=True)
    publisher = models.TextField(null=True)
    record_label = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    hash_audio = models.TextField(null=True)
    hash_compressed = models.TextField(null=True)

    def __str__(self) -> str:
        return f"[{self.label}] {self.display_artist} - {self.title}"


class AudioUploadJob(models.Model):
    """
    Job status tracker for audio uploads.
    """

    class AudioUploadStatus(models.TextChoices):
        QUEUED = "QUEUED", _("Queued for upload")
        ERROR = "ERROR", _("Error")
        VALIDATING = "VALIDATING", _("Confirming the file is an audio file")
        DECOMPRESSING = "DECOMPRESSING", _("Decompressing the audio")
        METADATA = "METADATA", _("Extracting metadata")
        COMPRESSING = "COMPRESSING", _("Generating compressed version")
        DONE = "DONE", _("Successfully processed the audio")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=13,
        choices=AudioUploadStatus.choices,
        default=AudioUploadStatus.QUEUED,
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    error = models.TextField(null=True)
