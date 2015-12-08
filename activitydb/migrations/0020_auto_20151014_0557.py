# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('activitydb', '0019_projectagreement_community_project_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='TolaUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='approvalauthority',
            name='approval_user',
            field=models.ForeignKey(related_name='auth_approving', blank=True, to='activitydb.TolaUser', help_text='User with Approval Authority', null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='approved_by',
            field=models.ForeignKey(related_name='comm_approving', blank=True, to='activitydb.TolaUser', help_text='This is the Provincial Line Manager', null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='filled_by',
            field=models.ForeignKey(related_name='comm_estimate', blank=True, to='activitydb.TolaUser', help_text='This is the originator', null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='location_verified_by',
            field=models.ForeignKey(related_name='comm_gis', blank=True, to='activitydb.TolaUser', help_text='This should be GIS Manager', null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='submitter',
            field=models.ForeignKey(to='activitydb.TolaUser'),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='approval_submitted_by',
            field=models.ForeignKey(related_name='submitted_by_agreement', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='approved_by',
            field=models.ForeignKey(related_name='approving_agreement', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='checked_by',
            field=models.ForeignKey(related_name='checking', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='estimated_by',
            field=models.ForeignKey(related_name='estimating', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='finance_reviewed_by',
            field=models.ForeignKey(related_name='finance_reviewing', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='me_reviewed_by',
            field=models.ForeignKey(related_name='reviewing_me', verbose_name='M&E Reviewed by', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='reviewed_by',
            field=models.ForeignKey(related_name='reviewing', verbose_name='Field Verification By', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='approval_submitted_by',
            field=models.ForeignKey(related_name='submitted_by_complete', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='approved_by',
            field=models.ForeignKey(related_name='approving_agreement_complete', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='checked_by',
            field=models.ForeignKey(related_name='checking_complete', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='estimated_by',
            field=models.ForeignKey(related_name='estimating_complete', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='reviewed_by',
            field=models.ForeignKey(related_name='reviewing_complete', blank=True, to='activitydb.TolaUser', null=True),
        ),
    ]
