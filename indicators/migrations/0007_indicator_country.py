# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0014_auto_20150803_1539'),
        ('indicators', '0006_auto_20150807_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='country',
            field=models.ForeignKey(default=1, blank=True, to='activitydb.Country'),
            preserve_default=False,
        ),
    ]
