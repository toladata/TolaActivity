# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0004_auto_20150622_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentationapp',
            name='project_agreement',
        ),
        migrations.RemoveField(
            model_name='programdashboard',
            name='project_agreement_count',
        ),
        migrations.RemoveField(
            model_name='programdashboard',
            name='project_agreement_count_approved',
        ),
        migrations.RemoveField(
            model_name='programdashboard',
            name='project_completion_count',
        ),
        migrations.RemoveField(
            model_name='programdashboard',
            name='project_completion_count_approved',
        ),
        migrations.AlterField(
            model_name='community',
            name='literacy_rate',
            field=models.IntegerField(null=True, verbose_name='Literacy Rate (%)', blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='literate_females',
            field=models.IntegerField(null=True, verbose_name='Number of Literate Females', blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='literate_males',
            field=models.IntegerField(null=True, verbose_name='Number of Literate Males', blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='total_literate_peoples',
            field=models.IntegerField(null=True, verbose_name='Total Literate People', blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='total_num_households',
            field=models.IntegerField(null=True, verbose_name='Total # Households', blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='village',
            field=models.CharField(max_length=255, null=True, verbose_name='Village', blank=True),
        ),
    ]
