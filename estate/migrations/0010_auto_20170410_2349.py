# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 22:49
from __future__ import unicode_literals

from django.db import migrations, models
import estate.utils


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0009_auto_20170410_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='floor',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='place',
            name='monthly_charges',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='property_tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='otherfield',
            name='field_type',
            field=models.CharField(choices=[('t', 'Text'), ('n', 'Number'), ('c', 'Currency')], default='t', max_length=1),
        ),
        migrations.AlterField(
            model_name='place',
            name='image',
            field=models.ImageField(blank=True, help_text='display image', null=True, upload_to=estate.utils.upload_thumbnail_dir, verbose_name='Display Image'),
        ),
        migrations.AlterField(
            model_name='place',
            name='thumbnail',
            field=models.ImageField(blank=True, help_text='image thumbnail', null=True, upload_to=estate.utils.upload_display_image_dir, verbose_name='Image thumbnail'),
        ),
    ]
