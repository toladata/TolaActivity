# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0061_auto_20160202_0706'),
        ('indicators', '0028_collecteddata_site'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collecteddata',
            name='site',
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='site',
            field=models.ManyToManyField(to='activitydb.SiteProfile', blank=True),
        ),
    ]
