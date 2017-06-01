# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-14 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0023_auto_20170514_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingschedule',
            name='email',
            field=models.EmailField(error_messages={'required': 'ce champ est requis'}, max_length=50, verbose_name='Votre email'),
        ),
        migrations.AlterField(
            model_name='bookingschedule',
            name='first_name',
            field=models.CharField(error_messages={'required': 'ce champ est requis'}, max_length=30, verbose_name='Prénom'),
        ),
        migrations.AlterField(
            model_name='bookingschedule',
            name='last_name',
            field=models.CharField(error_messages={'required': 'ce champ est requis'}, max_length=30, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='bookingschedule',
            name='message',
            field=models.TextField(error_messages={'required': 'ce champ est requis'}, verbose_name='votre message'),
        ),
        migrations.AlterField(
            model_name='bookingschedule',
            name='phone_number',
            field=models.CharField(error_messages={'required': 'ce champ est requis'}, max_length=15, verbose_name='Votre numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='bookingschedule',
            name='schedule_date',
            field=models.DateField(error_messages={'required': 'ce champ est requis'}, verbose_name='Date du calendrier'),
        ),
    ]
