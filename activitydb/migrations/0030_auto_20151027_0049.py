# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0029_auto_20151027_0041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='in_file',
        ),
        migrations.RemoveField(
            model_name='checklist',
            name='not_applicable',
        ),
        migrations.RemoveField(
            model_name='checklistitem',
            name='country',
        ),
        migrations.AddField(
            model_name='checklist',
            name='country',
            field=models.ForeignKey(blank=True, to='activitydb.Country', null=True),
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='in_file',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='not_applicable',
            field=models.BooleanField(default=False),
        ),
    ]
