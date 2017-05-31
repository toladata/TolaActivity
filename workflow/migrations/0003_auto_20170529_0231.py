# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-29 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_auto_20170522_0819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvalauthority',
            options={'ordering': ('approval_user',), 'verbose_name_plural': 'Approval Authority'},
        ),
        migrations.RemoveField(
            model_name='approvalauthority',
            name='fund',
        ),
        migrations.AddField(
            model_name='approvalauthority',
            name='workflowlevel1',
            field=models.ManyToManyField(blank=True, to='workflow.WorkflowLevel1'),
        ),
    ]
