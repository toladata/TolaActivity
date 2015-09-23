# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='activity_code',
            field=models.CharField(help_text=b'If applicable at this stage, please request Activity Code from MEL', max_length=255, null=True, verbose_name=b'Activity Code', blank=True),
        ),
    ]
