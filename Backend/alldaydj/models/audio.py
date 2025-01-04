from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    BooleanField,
    CASCADE,
    DateTimeField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    SET_NULL,
    TextField,
    UUIDField,
)
from uuid import uuid4


class Genre(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    genre = TextField(unique=True)


class Tag(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    tag = TextField(unique=True)


class Cart(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    label = TextField(blank=True, null=True, unique=True)
    artist = TextField(blank=True)
    title = TextField(blank=True)
    album = TextField(blank=True)
    genre = ForeignKey(Genre, on_delete=SET_NULL, null=True)
    year = IntegerField(
        null=True, validators=[MinValueValidator(1800), MaxValueValidator(9999)]
    )
    tags = ManyToManyField(Tag)
    sweeper = BooleanField(default=False)
    override_fade = BooleanField(default=False)
    valid_from = DateTimeField(null=True)
    valid_until = DateTimeField(null=True)
    isrc = TextField(blank=True)
    record_label = TextField(blank=True)


class DayPart(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = ForeignKey(Cart, on_delete=CASCADE)
    hour = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    day = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])
    permitted = BooleanField(default=True)
    unique_together = ("cart", "hour", "day")
