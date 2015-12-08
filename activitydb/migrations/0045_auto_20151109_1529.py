# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0044_auto_20151109_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='dashboard_name',
            field=models.ForeignKey(blank=True, to='activitydb.CustomDashboard', null=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='dashboard_name',
            field=models.ForeignKey(blank=True, to='activitydb.CustomDashboard', null=True),
        ),
    ]
