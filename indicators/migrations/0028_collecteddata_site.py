# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0060_auto_20160125_1752'),
        ('indicators', '0027_auto_20160126_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteddata',
            name='site',
            field=models.ForeignKey(blank=True, to='activitydb.SiteProfile', null=True),
        ),
    ]
