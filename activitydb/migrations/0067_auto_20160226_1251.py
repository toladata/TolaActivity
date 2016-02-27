# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0066_auto_20160216_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='sector',
        ),
        migrations.AddField(
            model_name='program',
            name='sector',
            field=models.ManyToManyField(to='activitydb.Sector', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='activity_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Activity Code', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='estimated_num_direct_beneficiaries',
            field=models.CharField(help_text="Please provide achievable estimates as we will use these as our 'Targets'", max_length=255, null=True, verbose_name='Estimated number of direct beneficiaries', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='project_description',
            field=models.TextField(null=True, verbose_name='Project Description', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='project_type',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectType', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='staff_responsible',
            field=models.CharField(max_length=255, null=True, verbose_name='Staff Responsible', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_start_date',
            field=models.DateTimeField(help_text='Imported from Project Agreement', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='capacity_built',
            field=models.TextField(max_length=755, null=True, verbose_name='Describe how sustainability was ensured for this project?', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='expected_duration',
            field=models.CharField(help_text='Imported from Project Agreement', max_length=255, null=True, verbose_name='Expected Duration', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='expected_end_date',
            field=models.DateTimeField(help_text='Imported Project Agreement', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='expected_start_date',
            field=models.DateTimeField(help_text='Imported Project Agreement', null=True, blank=True),
        ),
    ]
