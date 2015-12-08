# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0016_auto_20150924_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcomplete',
            name='account_code',
            field=models.CharField(max_length=255, null=True, verbose_name='Account Code', blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='agency_cost',
            field=models.CharField(help_text='In USD', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='exchange_rate',
            field=models.CharField(help_text='Local Currency exchange rate to USD', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='exchange_rate_date',
            field=models.DateField(help_text='Date of exchange rate', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='lin_code',
            field=models.CharField(max_length=255, null=True, verbose_name='LIN Sub Code', blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='local_agency_cost',
            field=models.CharField(help_text='Total portion of cost for your agency', max_length=255, null=True, verbose_name='Organization Total in Local Currency', blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='local_total_cost',
            field=models.CharField(help_text='In Local Currency', max_length=255, null=True, verbose_name='Total in Local Currency', blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='project_type',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectType', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='sector',
            field=models.ForeignKey(blank=True, to='activitydb.Sector', null=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='total_cost',
            field=models.CharField(help_text='In USD', max_length=255, null=True, blank=True),
        ),
    ]
