# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0051_auto_20151209_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='local_mc_estimated_budget',
            field=models.DecimalField(default=Decimal('0.00'), help_text='Total portion of estimate for your agency', verbose_name='Estimated Organization Total in Local Currency', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='local_total_estimated_budget',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In Local Currency', verbose_name='Estimated Total in Local Currency', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='mc_estimated_budget',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In USD', verbose_name='Organizations portion of Project Budget', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='total_estimated_budget',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In USD', verbose_name='Total Project Budget', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_budget',
            field=models.DecimalField(default=Decimal('0.00'), help_text='What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit', verbose_name='Actual Cost', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='agency_cost',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In USD', verbose_name='Actual Cost for Organization', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='estimated_budget',
            field=models.DecimalField(default=Decimal('0.00'), verbose_name='Estimated Budget', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='local_agency_cost',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In Local Currency', verbose_name='Actual Cost for Organization', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='local_total_cost',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In Local Currency', verbose_name='Actual Cost', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='total_cost',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In USD', verbose_name='Estimated Budget for Organization', max_digits=12, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='avg_household_size',
            field=models.DecimalField(default=Decimal('0.00'), verbose_name='Average Household Size', max_digits=25, decimal_places=14),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='avg_landholding_size',
            field=models.DecimalField(default=Decimal('0.00'), help_text='In hectares/jeribs', verbose_name='Average Landholding Size', max_digits=25, decimal_places=14),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='latitude',
            field=models.DecimalField(default=Decimal('0.00'), verbose_name='Latitude (Decimal Coordinates)', max_digits=25, decimal_places=14),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='longitude',
            field=models.DecimalField(default=Decimal('0.00'), verbose_name='Longitude (Decimal Coordinates)', max_digits=25, decimal_places=14),
        ),
    ]
