# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0018_auto_20151113_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collecteddata',
            name='analysis_name',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='date_of_analysis',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='date_of_training',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='method',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='office',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='tool',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='trainer_name',
        ),
        migrations.AddField(
            model_name='externalservice',
            name='feed_url',
            field=models.CharField(max_length=765, blank=True),
        ),
    ]
