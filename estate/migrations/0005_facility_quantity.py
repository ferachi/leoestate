# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0004_auto_20170312_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
