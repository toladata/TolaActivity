# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0019_projectagreement_community_project_description'),
        ('indicators', '0009_auto_20150928_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteddata',
            name='program',
            field=models.ForeignKey(related_name='i_program', blank=True, to='activitydb.Program', null=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='disaggregation',
            field=models.ManyToManyField(to='indicators.DisaggregationType', blank=True),
        ),
    ]
