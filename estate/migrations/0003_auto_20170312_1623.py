# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 15:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0002_auto_20170312_1553'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SalePlace',
            new_name='BuyablePlace',
        ),
        migrations.RenameModel(
            old_name='RentedPlace',
            new_name='RentablePlace',
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'verbose_name_plural': 'facilities'},
        ),
    ]
