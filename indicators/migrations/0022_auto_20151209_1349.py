# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0021_auto_20151204_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='complete',
            field=models.ForeignKey(related_name='q_complete2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='activitydb.ProjectComplete', null=True),
        ),
    ]
