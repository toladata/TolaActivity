# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customdashboard', '0004_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programnarrative',
            name='program',
        ),
        migrations.AlterField(
            model_name='gallery',
            name='narrative',
            field=models.TextField(max_length=200, verbose_name=b'Narrative Text', blank=True),
        ),
        migrations.DeleteModel(
            name='ProgramNarrative',
        ),
    ]
