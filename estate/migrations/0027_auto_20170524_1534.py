# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-24 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0026_clientproperty_formdownload'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientproperty',
            name='facilities',
            field=models.ManyToManyField(related_name='client_properties', to='estate.Facility'),
        ),
        migrations.AlterField(
            model_name='clientproperty',
            name='selling_status',
            field=models.CharField(choices=[('a', 'Oui, j’ai déjà commencé la vente'), ('b', 'Oui, dès que possible'), ('c', 'Oui, d’ici 3 mois'), ('d', 'Oui, d’ici 6 mois'), ('e', 'Oui, dans plus de 6 mois'), ('f', 'Non, je n’ai pas de projet de vente')], default='a', max_length=1, verbose_name='Envisagez-vous de vendre ce bien ?'),
        ),
    ]