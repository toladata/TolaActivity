# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0057_auto_20151228_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminlevelthree',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Admin Level 3', blank=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Admin Level 2', blank=True),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Admin Level 1', blank=True),
        ),
        migrations.AlterField(
            model_name='village',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Admin Level 4', blank=True),
        ),
    ]
