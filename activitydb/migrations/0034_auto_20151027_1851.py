# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0033_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='project_description',
            field=models.TextField(help_text='Description must meet the Criteria.  Will translate description into three languages: English, Dari and Pashto)', null=True, verbose_name='Project Description', blank=True),
        ),
        migrations.AlterField(
            model_name='stakeholder',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Stakeholder/Organization Name', blank=True),
        ),
    ]
