# Generated by Django 3.1.3 on 2020-11-20 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alldaydj", "0003_audiouploadjob"),
    ]

    operations = [
        migrations.AddField(
            model_name="audiouploadjob",
            name="error",
            field=models.TextField(null=True),
        ),
    ]