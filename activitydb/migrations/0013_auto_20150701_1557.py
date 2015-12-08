# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0012_auto_20150630_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='capacity',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='capacity',
            field=models.ManyToManyField(max_length=255, null=True, to='activitydb.Capacity', blank=True),
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='evaluate',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='evaluate',
            field=models.ManyToManyField(max_length=255, null=True, to='activitydb.Evaluate', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='project_description',
            field=models.TextField(help_text='Description must meet the Criteria.  Will translate description into three languages: English, Dari and Pashto', null=True, verbose_name='Project Description', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='project_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Project Name', blank=True),
        ),
    ]
