# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0030_auto_20160206_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='strategic_objectives',
            field=models.ManyToManyField(related_name='strat_indicator', verbose_name=b'Country Strategic Objective', to='indicators.StrategicObjective', blank=True),
        ),
    ]
