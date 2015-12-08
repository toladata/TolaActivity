# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0031_checklist_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='mc_objectives',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='program_objectives',
        ),
    ]
