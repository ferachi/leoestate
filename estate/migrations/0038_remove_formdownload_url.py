# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 08:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0037_auto_20170601_0642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdownload',
            name='url',
        ),
    ]
