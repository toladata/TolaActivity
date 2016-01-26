# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0059_projectagreement_risks_assumptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='risks_assumptions',
            field=models.TextField(null=True, verbose_name='Risks and Assumptions', blank=True),
        ),
    ]
