# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0033_historicalcollecteddata_historicalindicator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='objectives',
            field=models.ManyToManyField(related_name='obj_indicator', verbose_name=b'Program Objective', to='indicators.Objective', blank=True),
        ),
    ]
