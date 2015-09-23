# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0006_auto_20150625_1636'),
        ('indicators', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='objective',
            name='country',
            field=models.ForeignKey(blank=True, to='activitydb.Country', null=True),
        ),
    ]
