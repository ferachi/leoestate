# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 21:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0020_bookingdate_bookingschedule'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookingdate',
            options={'ordering': ['scheduled_date']},
        ),
    ]