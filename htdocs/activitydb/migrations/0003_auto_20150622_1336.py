# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0002_auto_20150622_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='community_mobilizer',
            field=models.CharField(max_length=255, null=True, verbose_name=b'MC Community Mobilizer', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='community_mobilizer_contact',
            field=models.CharField(max_length=255, null=True, verbose_name=b'MC Community Mobilizer Contact Number', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='community_rep',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Community Representative', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='community_rep_contact',
            field=models.CharField(help_text=b'Can have mulitple contact numbers', max_length=255, null=True, verbose_name=b'Community Representative Contact', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='has_rej_letter',
            field=models.BooleanField(default=False, help_text=b'If yes attach copy', verbose_name=b'If Rejected: Rejection Letter Sent?'),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='rejection_letter',
            field=models.FileField(upload_to=b'uploads', null=True, verbose_name=b'Rejection Letter', blank=True),
        ),
    ]
