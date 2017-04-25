# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0015_auto_20170414_1442'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='vote',
            name='rating',
        ),
        migrations.AddField(
            model_name='vote',
            name='is_like',
            field=models.NullBooleanField(),
        ),
    ]