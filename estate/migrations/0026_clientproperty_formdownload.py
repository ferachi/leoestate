# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-23 16:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0025_auto_20170520_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(choices=[('MV', 'Maison/Villa'), ('AP', 'Apartement')], default='MV', max_length=2, verbose_name='Type de bien')),
                ('no_rooms', models.CharField(choices=[('a', '1'), ('b', '2'), ('c', '3'), ('d', '4'), ('e', '5'), ('f', '6 et +')], default='a', max_length=1, verbose_name='Nombre de pièce(s)')),
                ('land_area', models.CharField(max_length=8, verbose_name='Surface terrain')),
                ('no_bathrooms', models.CharField(choices=[('a', '1'), ('b', '2'), ('c', '3'), ('d', '4'), ('e', '5'), ('f', '6 et +')], default='a', max_length=1, verbose_name='Nombre de salle de bains')),
                ('area', models.CharField(max_length=8, verbose_name='Surface')),
                ('price', models.CharField(max_length=8, verbose_name='Prix demandé')),
                ('address', models.CharField(max_length=400, verbose_name='Nom de la rue')),
                ('postal_code', models.CharField(max_length=6, verbose_name='Code postal')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('year_constructed', models.CharField(max_length=4, verbose_name='Année de construction')),
                ('selling_status', models.CharField(choices=[('a', 'Oui, j’ai déjà commencé la vente'), ('b', 'Oui, dès que possible'), ('c', 'Oui, d’ici 3 mois'), ('d', 'Oui, d’ici 6 mois'), ('e', 'Oui, dans plus de 6 mois'), ('f', 'Non, je n’ai pas de projet de vente')], default='a', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='FormDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_downloaded', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=False)),
                ('url', models.URLField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estate.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estate.UserProfile')),
            ],
        ),
    ]
