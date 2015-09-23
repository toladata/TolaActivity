# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0008_projectagreement_community_proposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='project_name',
            field=models.CharField(help_text='Please be specific in your name.  Consider that your Project Name includes WHO, WHAT, WHERE, HOW', max_length=255, verbose_name='Project Name'),
        ),
    ]
