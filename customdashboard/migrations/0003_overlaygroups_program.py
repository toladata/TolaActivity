# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customdashboard', '0002_overlaygroups_overlaynarratives'),
    ]

    operations = [
        migrations.AddField(
            model_name='overlaygroups',
            name='program',
            field=models.ForeignKey(default=int(1), blank=True, to='activitydb.Program'),
            preserve_default=False,
        ),
    ]
