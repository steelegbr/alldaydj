from django.contrib.postgres.operations import CITextExtension
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0002_auto_20201117_0806"),
    ]

    operations = [CITextExtension()]
