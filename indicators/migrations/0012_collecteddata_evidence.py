# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0019_projectagreement_community_project_description'),
        ('indicators', '0011_auto_20151001_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteddata',
            name='evidence',
            field=models.ForeignKey(blank=True, to='activitydb.Documentation', null=True),
        ),
    ]
