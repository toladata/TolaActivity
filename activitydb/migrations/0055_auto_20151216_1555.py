# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0054_auto_20151215_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalauthority',
            name='fund',
            field=models.CharField(max_length='255', null=True, verbose_name='Fund', blank=True),
        ),
    ]
