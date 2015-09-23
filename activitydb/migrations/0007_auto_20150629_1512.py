# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0006_auto_20150625_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='num_animals_population_owning',
        ),
        migrations.AddField(
            model_name='community',
            name='altitude',
            field=models.DecimalField(null=True, verbose_name='Altitude (in meters)', max_digits=25, decimal_places=14, blank=True),
        ),
        migrations.AddField(
            model_name='community',
            name='location_verified_by',
            field=models.ForeignKey(related_name='comm_gis', blank=True, to=settings.AUTH_USER_MODEL, help_text='This should be GIS Manager', null=True),
        ),
        migrations.AddField(
            model_name='community',
            name='precision',
            field=models.DecimalField(null=True, verbose_name='Precision (in meters)', max_digits=25, decimal_places=14, blank=True),
        ),
        migrations.AddField(
            model_name='community',
            name='total_female',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='community',
            name='total_male',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='animal_type',
            field=models.CharField(help_text='List Animal Types', max_length=255, null=True, verbose_name='Animal Types', blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='contact_number',
            field=models.CharField(max_length=255, null=True, verbose_name='Contact Number', blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='latitude',
            field=models.DecimalField(null=True, verbose_name='Latitude (Decimal Coordinates)', max_digits=25, decimal_places=14, blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='longitude',
            field=models.DecimalField(null=True, verbose_name='Longitude (Decimal Coordinates)', max_digits=25, decimal_places=14, blank=True),
        ),
        migrations.AlterField(
            model_name='profiletype',
            name='profile',
            field=models.CharField(max_length=255, verbose_name='Profile Type', blank=True),
        ),
    ]
