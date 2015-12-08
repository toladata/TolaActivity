# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0008_auto_20150923_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='disaggregation',
        ),
        migrations.AddField(
            model_name='indicator',
            name='disaggregation',
            field=models.ManyToManyField(to='indicators.DisaggregationType', null=True, blank=True),
        ),
    ]
