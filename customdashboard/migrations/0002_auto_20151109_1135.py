# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customdashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customdashboard',
            name='program',
        ),
        migrations.RemoveField(
            model_name='customdashboard',
            name='project_agreement',
        ),
        migrations.RemoveField(
            model_name='customdashboard',
            name='project_completion',
        ),
        migrations.AlterField(
            model_name='projectstatus',
            name='description',
            field=models.CharField(max_length=200, verbose_name=b'Status Description', blank=True),
        ),
        migrations.AlterField(
            model_name='projectstatus',
            name='project_status',
            field=models.CharField(max_length=50, verbose_name=b'Project Status', blank=True),
        ),
        migrations.DeleteModel(
            name='CustomDashboard',
        ),
    ]
