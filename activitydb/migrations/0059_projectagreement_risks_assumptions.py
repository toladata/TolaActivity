# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0058_auto_20160107_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='risks_assumptions',
            field=models.TextField(null=True, verbose_name='Ricks and Assumptions', blank=True),
        ),
    ]
