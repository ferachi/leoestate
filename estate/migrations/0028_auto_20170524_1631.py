# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-24 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0027_auto_20170524_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientproperty',
            name='facilities',
        ),
        migrations.AddField(
            model_name='clientproperty',
            name='facilities',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
