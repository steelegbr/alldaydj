from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    BooleanField,
    CASCADE,
    DateTimeField,
    FloatField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    SET_NULL,
    TextField,
    UUIDField,
)
from typing import List
from uuid import uuid4


class Genre(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    genre = TextField(unique=True)

    def __str__(self):
        return self.genre


class Tag(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    tag = TextField(unique=True)

    def __str__(self):
        return self.tag


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
    cue_start = FloatField()
    cue_intro = FloatField(null=True)
    cue_outro = FloatField()

    def __str__(self):
        return f"({self.label}) {self.artist} - {self.title}"

    def clean(self):
        errors: List[ValidationError] = []

        if self.cue_intro and self.cue_intro < self.cue_start:
            errors.append(
                ValidationError(
                    "Intro cue of %(intro)f must come after start cue of %(start)f",
                    params={"intro": self.cue_intro, "start": self.cue_start},
                )
            )

        if self.cue_intro and self.cue_intro > self.cue_outro:
            errors.append(
                ValidationError(
                    "Intro cue of %(intro)f must come before outro cue of %(outro)f",
                    params={"intro": self.cue_intro, "outro": self.cue_outro},
                )
            )

        if self.cue_start > self.cue_outro:
            errors.append(
                ValidationError(
                    "Start cue of %(start)f must come before outro cue of %(outro)f",
                    params={"start": self.cue_start, "outro": self.cue_outro},
                )
            )

        if self.valid_from and self.valid_until and self.valid_from > self.valid_until:
            errors.append(
                ValidationError(
                    "Valid from date of %(from)s must come before valid until date of %(until)s",
                    params={"from": self.valid_from, "until": self.valid_until},
                )
            )

        if errors:
            raise ValidationError(errors)


class DayPart(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = ForeignKey(Cart, on_delete=CASCADE)
    hour = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    day = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])
    permitted = BooleanField(default=True)
    unique_together = ("cart", "hour", "day")
