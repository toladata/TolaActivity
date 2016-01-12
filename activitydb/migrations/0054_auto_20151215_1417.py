# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0053_auto_20151211_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='customdashboard',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='External Public Dashboard'),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='local_mc_estimated_budget',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='Total portion of estimate for your agency', verbose_name='Estimated Organization Total in Local Currency'),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='local_total_estimated_budget',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='In Local Currency', verbose_name='Estimated Total in Local Currency'),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='mc_estimated_budget',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='In USD', verbose_name='Organizations portion of Project Budget'),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='total_estimated_budget',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='In USD', verbose_name='Total Project Budget'),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_budget',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20, blank=True, help_text='What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit', verbose_name='Actual Cost'),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='agency_cost',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='In USD', verbose_name='Actual Cost for Organization'),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='estimated_budget',
            field=models.DecimalField(default=Decimal('0.00'), verbose_name='Estimated Budget', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='local_agency_cost',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='In Local Currency', verbose_name='Actual Cost for Organization'),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='local_total_cost',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='In Local Currency', verbose_name='Actual Cost'),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, blank=True, help_text='In USD', verbose_name='Estimated Budget for Organization'),
        ),
    ]
