# Generated by Django 4.2 on 2023-09-14 10:38

import bboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0003_bb_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='archive',
            field=models.FileField(blank=True, upload_to=bboard.models.get_timestamp_path),
        ),
    ]