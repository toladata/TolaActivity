# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0010_auto_20150629_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='cfw_estimate_cost_materials',
            field=models.CharField(max_length='255', null=True, verbose_name='Estimated Total Cost of Materials', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='cfw_estimate_female',
            field=models.IntegerField(null=True, verbose_name='Estimated # of Female Laborers', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='cfw_estimate_male',
            field=models.IntegerField(null=True, verbose_name='Estimated # of Male Laborers', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='cfw_estimate_person_days',
            field=models.IntegerField(null=True, verbose_name='Estimated # of Person Days', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='cfw_estimate_project_days',
            field=models.IntegerField(null=True, verbose_name='Estimated # of Project Days', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='cfw_estimate_total',
            field=models.IntegerField(null=True, verbose_name='Estimated Total # of Laborers', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='cfw_estimate_wages_budgeted',
            field=models.CharField(max_length='255', null=True, verbose_name='Estimated Wages Budgeted', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='distribution_estimate',
            field=models.CharField(max_length='255', null=True, verbose_name='Estimated # of Items Distributed', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='distribution_type',
            field=models.CharField(max_length='255', null=True, verbose_name='Type of Items Distributed', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='distribution_uom',
            field=models.CharField(max_length='255', null=True, verbose_name='Unit of Measure', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='estimate_female_trained',
            field=models.IntegerField(null=True, verbose_name='Estimated # of Female Trained', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='estimate_male_trained',
            field=models.IntegerField(null=True, verbose_name='Estimated # of Male Trained', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='estimate_total_trained',
            field=models.IntegerField(null=True, verbose_name='Estimated Total # Trained', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='estimate_trainings',
            field=models.IntegerField(null=True, verbose_name='Estimated # of Trainings Conducted', blank=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='project_description',
            field=models.TextField(null=True, verbose_name='Project Description', blank=True),
        ),
    ]
