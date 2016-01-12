# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0049_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classify_land', models.CharField(help_text='Rural, Urban, Peri-Urban', max_length=100, verbose_name='Land Classification', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('classify_land',),
            },
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='actual_cost_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='quality_assured',
            field=models.TextField(max_length=755, null=True, verbose_name='How was quality assured for this project', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='approval',
            field=models.CharField(default='in progress', max_length=255, null=True, verbose_name='Approval Status', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_budget',
            field=models.CharField(help_text='What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit', max_length=255, null=True, verbose_name='Actual Cost', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='agency_cost',
            field=models.CharField(help_text='In USD', max_length=255, null=True, verbose_name='Actual Cost for Organization', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='approval',
            field=models.CharField(default='in progress', max_length=255, null=True, verbose_name='Approval Status', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='budget_variance',
            field=models.CharField(max_length=255, null=True, verbose_name='Budget versus Actual variance', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='capacity_built',
            field=models.TextField(max_length=755, null=True, verbose_name='Describe ow sustainability was ensured for this project?', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='estimated_budget',
            field=models.CharField(max_length=255, null=True, verbose_name='Estimated Budget', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='local_agency_cost',
            field=models.CharField(help_text='In Local Currency', max_length=255, null=True, verbose_name='Actual Cost for Organization', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='local_total_cost',
            field=models.CharField(help_text='In Local Currency', max_length=255, null=True, verbose_name='Actual Cost', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='total_cost',
            field=models.CharField(help_text='In USD', max_length=255, null=True, verbose_name='Estimated Budget for Organization', blank=True),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='classify_land',
            field=models.ForeignKey(blank=True, to='activitydb.LandType', null=True),
        ),
    ]
