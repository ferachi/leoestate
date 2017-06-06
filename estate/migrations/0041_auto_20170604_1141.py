# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-04 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0040_formdownload_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdownload',
            name='document',
        ),
        migrations.AddField(
            model_name='propertydocument',
            name='is_downloaded',
            field=models.BooleanField(default=True),
        ),
    ]