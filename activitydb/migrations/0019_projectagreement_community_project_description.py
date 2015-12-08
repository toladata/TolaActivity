# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0018_auto_20150925_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='community_project_description',
            field=models.TextField(help_text='Description must describe how the Community Proposal meets the project criteria', null=True, verbose_name='Describe the project you would like the program to consider', blank=True),
        ),
    ]
