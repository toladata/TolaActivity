# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0005_auto_20150807_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='indicator_type',
            field=models.ManyToManyField(to='indicators.IndicatorType', blank=True),
        ),
    ]
