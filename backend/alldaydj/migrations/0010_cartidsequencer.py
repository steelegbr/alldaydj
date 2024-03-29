# Generated by Django 3.2.9 on 2021-11-01 20:34

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("alldaydj", "0009_remove_cart_cue_intro_start"),
    ]

    operations = [
        migrations.CreateModel(
            name="CartIdSequencer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.TextField(unique=True)),
                (
                    "prefix",
                    models.TextField(
                        validators=[
                            django.core.validators.RegexValidator("[a-zA-Z0-9]*")
                        ]
                    ),
                ),
                (
                    "suffix",
                    models.TextField(
                        validators=[
                            django.core.validators.RegexValidator("[a-zA-Z0-9]*")
                        ]
                    ),
                ),
                (
                    "min_digits",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
            ],
        ),
    ]
