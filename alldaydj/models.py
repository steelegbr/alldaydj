"""
    Models for AllDay DJ
"""

from colorfield.fields import ColorField
from django.contrib.postgres.fields import CITextField
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
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

    def __str__(self) -> str:
        return f"[{self.label}] {self.display_artist} - {self.title}"
