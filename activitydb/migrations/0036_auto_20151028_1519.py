# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0035_auto_20151028_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='capacity',
            field=models.ManyToManyField(to='activitydb.Capacity', verbose_name='Sustainability Plan', blank=True),
        ),
    ]
