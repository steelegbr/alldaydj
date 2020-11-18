# Generated by Django 3.1.3 on 2020-11-18 07:57

import colorfield.fields
import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', django.contrib.postgres.fields.citext.CITextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tag', django.contrib.postgres.fields.citext.CITextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', django.contrib.postgres.fields.citext.CITextField(unique=True)),
                ('colour', colorfield.fields.ColorField(default='#AC1AF7', max_length=18)),
                ('now_playing', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label', django.contrib.postgres.fields.citext.CITextField(unique=True, validators=[django.core.validators.RegexValidator('[a-zA-Z0-9]+')])),
                ('title', models.TextField()),
                ('display_artist', models.TextField()),
                ('cue_audio_start', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cue_audio_end', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cue_intro_start', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cue_intro_end', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('cue_segue', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('sweeper', models.BooleanField(default=False)),
                ('year', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('isrc', models.TextField()),
                ('composer', models.TextField()),
                ('publisher', models.TextField()),
                ('record_label', models.TextField()),
                ('artists', models.ManyToManyField(to='alldaydj.Artist')),
                ('tags', models.ManyToManyField(to='alldaydj.Tag')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='alldaydj.type')),
            ],
        ),
    ]
