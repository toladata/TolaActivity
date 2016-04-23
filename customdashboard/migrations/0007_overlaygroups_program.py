# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0073_auto_20160317_1329'),
        ('customdashboard', '0006_overlaygroups_overlaynarratives'),
    ]

    operations = [
        migrations.AddField(
            model_name='overlaygroups',
            name='program',
            field=models.ForeignKey(default=int(1), blank=True, to='activitydb.Program'),
            preserve_default=False,
        ),
    ]
