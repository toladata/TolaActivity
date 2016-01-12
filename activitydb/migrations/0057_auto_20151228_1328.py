# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0056_program_budget_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcomplete',
            name='project_agreement',
            field=models.OneToOneField(to='activitydb.ProjectAgreement'),
        ),
    ]
