# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0024_auto_20151211_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='key_performance_indicator',
            field=models.BooleanField(default=False, verbose_name=b'Key Performance Indicator for this program?'),
        ),
    ]
