# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0047_auto_20151119_1131'),
        ('indicators', '0019_auto_20151117_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteddata',
            name='approved_by',
            field=models.ForeignKey(related_name='approving_data', verbose_name=b'Originated By', blank=True, to='activitydb.TolaUser', null=True),
        ),
    ]
