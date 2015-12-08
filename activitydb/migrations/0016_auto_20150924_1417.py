# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0015_auto_20150924_0646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectproposal',
            name='approval_submitted_by',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='community',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='estimated_by',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='office',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='program',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='project_type',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='sector',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='exchange_rate',
            field=models.CharField(help_text='Local Currency exchange rate to USD', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='exchange_rate_date',
            field=models.DateField(help_text='Date of exchange rate', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='local_mc_estimated_budget',
            field=models.CharField(help_text='Total portion of estimate for your agency', max_length=255, null=True, verbose_name='Estimated Organization Total in Local Currency', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='local_total_estimated_budget',
            field=models.CharField(help_text='In Local Currency', max_length=255, null=True, verbose_name='Estimated Total in Local Currency', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='account_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Account Code', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='lin_code',
            field=models.CharField(max_length=255, null=True, verbose_name='LIN Sub Code', blank=True),
        ),
        migrations.DeleteModel(
            name='ProjectProposal',
        ),
    ]
