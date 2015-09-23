# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0005_auto_20150623_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contribution',
            name='project_agreement',
        ),
        migrations.RemoveField(
            model_name='contribution',
            name='project_complete',
        ),
        migrations.DeleteModel(
            name='Contribution',
        ),
    ]
