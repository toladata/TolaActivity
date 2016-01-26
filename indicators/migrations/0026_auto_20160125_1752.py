# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0025_indicator_key_performance_indicator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='program',
            field=models.ManyToManyField(related_name='indicator_program', to='activitydb.Program'),
        ),
    ]
