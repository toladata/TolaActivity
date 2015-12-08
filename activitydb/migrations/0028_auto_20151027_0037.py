# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0027_auto_20151027_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='item',
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='checklist',
            field=models.ForeignKey(default=1, to='activitydb.Checklist'),
            preserve_default=False,
        ),
    ]
