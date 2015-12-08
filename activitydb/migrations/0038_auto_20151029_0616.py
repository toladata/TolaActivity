# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0037_auto_20151028_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='estimated_by',
            field=models.ForeignKey(related_name='estimating', verbose_name='Originated By', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='estimated_by_date',
            field=models.DateTimeField(null=True, verbose_name='Date Originated', blank=True),
        ),
    ]
