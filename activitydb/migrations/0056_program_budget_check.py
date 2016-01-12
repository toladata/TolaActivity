# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0055_auto_20151216_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='budget_check',
            field=models.BooleanField(default=False, verbose_name='Enable Approval Authority Matrix'),
        ),
    ]
