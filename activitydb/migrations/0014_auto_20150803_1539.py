# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0013_auto_20150701_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='capacity',
            field=models.ManyToManyField(to='activitydb.Capacity', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='evaluate',
            field=models.ManyToManyField(to='activitydb.Evaluate', blank=True),
        ),
    ]
