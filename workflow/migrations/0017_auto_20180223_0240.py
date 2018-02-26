# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-23 10:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0016_auto_20180209_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='currency_format',
            field=models.CharField(blank=True, default='Commas', max_length=50, verbose_name='Currency Format'),
        ),
        migrations.AddField(
            model_name='organization',
            name='date_format',
            field=models.CharField(blank=True, default='DD.MM.YYYY', max_length=50, verbose_name='Date Format'),
        ),
        migrations.AddField(
            model_name='organization',
            name='default_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow.Currency'),
        ),
        migrations.AddField(
            model_name='organization',
            name='default_language',
            field=models.CharField(blank=True, default='English', max_length=100, verbose_name='Default Language'),
        ),
    ]
