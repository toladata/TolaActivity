# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0021_adminlevelthree'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentation',
            name='program',
            field=models.ForeignKey(blank=True, to='activitydb.Program', null=True),
        ),
    ]
