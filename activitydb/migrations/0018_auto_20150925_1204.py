# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0017_auto_20150925_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcomplete',
            name='average_household_size',
            field=models.CharField(help_text='Refer to Form 01 - Community Profile', max_length=255, null=True, verbose_name='Average Household Size', blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='beneficiary_type',
            field=models.CharField(help_text='i.e. Farmer, Association, Student, Govt, etc.', max_length=255, null=True, verbose_name='Type of direct beneficiaries', blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='community_handover',
            field=models.BooleanField(default=None, help_text='Check box if it was completed', verbose_name='CommunityHandover/Sustainability Maintenance Plan'),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='community_involvement',
            field=models.CharField(max_length=255, null=True, verbose_name='Community Involvement', blank=True),
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='indirect_beneficiaries',
            field=models.CharField(help_text='This is a calculation - multiply direct beneficiaries by average household size', max_length=255, null=True, verbose_name='Estimated Number of indirect beneficiaries', blank=True),
        ),
    ]
