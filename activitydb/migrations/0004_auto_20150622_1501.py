# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0003_auto_20150622_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectagreement',
            options={'ordering': ('create_date',), 'permissions': (('can_approve', 'Can approve agreement'),)},
        ),
        migrations.RemoveField(
            model_name='mergemap',
            name='project_proposal',
        ),
        migrations.RemoveField(
            model_name='programdashboard',
            name='project_proposal',
        ),
        migrations.RemoveField(
            model_name='programdashboard',
            name='project_proposal_count',
        ),
        migrations.RemoveField(
            model_name='programdashboard',
            name='project_proposal_count_approved',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='project_proposal',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='project_proposal',
        ),
        migrations.RemoveField(
            model_name='trainingattendance',
            name='project_proposal',
        ),
        migrations.AddField(
            model_name='documentationapp',
            name='project_agreement',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True),
        ),
        migrations.AddField(
            model_name='trainingattendance',
            name='project_agreement',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True),
        ),
        migrations.AlterField(
            model_name='documentation',
            name='project',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True),
        ),
    ]
