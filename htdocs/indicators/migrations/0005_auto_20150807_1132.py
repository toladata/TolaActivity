# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0004_auto_20150803_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='indicator_type',
        ),
        migrations.AddField(
            model_name='indicator',
            name='indicator_type',
            field=models.ManyToManyField(to='indicators.IndicatorType', null=True, blank=True),
        ),
    ]
