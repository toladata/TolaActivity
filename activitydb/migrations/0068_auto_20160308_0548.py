# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0067_auto_20160226_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='lin_code',
            field=models.CharField(max_length=255, null=True, verbose_name='LIN Code', blank=True),
        ),
    ]
