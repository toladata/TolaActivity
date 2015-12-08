# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0014_auto_20150803_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='documentation_community_approval',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='documentation_government_approval',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='external_stakeholder_list',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='rejection_letter',
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='community_mobilizer',
            field=models.CharField(max_length=255, null=True, verbose_name='Community Mobilizer', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='community_mobilizer_contact',
            field=models.CharField(max_length=255, null=True, verbose_name='Community Mobilizer Contact Number', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='effect_or_impact',
            field=models.TextField(null=True, verbose_name='What is the anticipated Outcome or Goal?', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='justification_background',
            field=models.TextField(null=True, verbose_name='General Background and Problem Statement', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='justification_description_community_selection',
            field=models.TextField(null=True, verbose_name='Description of Stakeholder Selection Criteria', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='mc_objectives',
            field=models.TextField(null=True, verbose_name='What strategic Objectives does this help fulfill?', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='me_reviewed_by',
            field=models.ForeignKey(related_name='reviewing_me', verbose_name='M&E Reviewed by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='reviewed_by',
            field=models.ForeignKey(related_name='reviewing', verbose_name='Field Verification By', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='reviewed_by_date',
            field=models.DateTimeField(null=True, verbose_name='Date Verified', blank=True),
        ),
    ]
