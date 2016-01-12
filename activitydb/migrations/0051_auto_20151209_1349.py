# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0050_auto_20151208_1803'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectcomplete',
            options={'ordering': ('create_date',), 'verbose_name_plural': 'Project Completions'},
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='progress_against_targets',
            field=models.IntegerField(null=True, verbose_name='Progress against Targets (%)', blank=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='complete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='activitydb.ProjectComplete', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='mc_estimated_budget',
            field=models.CharField(help_text='In USD', max_length=255, null=True, verbose_name='Organizations portion of Project Budget', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='total_estimated_budget',
            field=models.CharField(help_text='In USD', max_length=255, null=True, verbose_name='Total Project Budget', blank=True),
        ),
    ]
