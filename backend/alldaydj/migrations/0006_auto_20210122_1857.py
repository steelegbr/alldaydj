# Generated by Django 3.1.5 on 2021-01-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alldaydj", "0005_auto_20210104_2035"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="audio",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="compressed",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="audiouploadjob",
            name="status",
            field=models.CharField(
                choices=[
                    ("QUEUED", "Queued for upload"),
                    ("ERROR", "Error"),
                    ("VALIDATING", "Confirming the file is an audio file"),
                    ("DECOMPRESSING", "Decompressing the audio"),
                    ("METADATA", "Extracting metadata"),
                    ("COMPRESSING", "Generating compressed version"),
                    ("HASHING", "Generating hashes"),
                    ("DONE", "Successfully processed the audio"),
                ],
                default="QUEUED",
                max_length=13,
            ),
        ),
    ]
