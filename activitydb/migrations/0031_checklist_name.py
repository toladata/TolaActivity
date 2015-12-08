# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0030_auto_20151027_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='name',
            field=models.CharField(default='Checklist', max_length=255, null=True, blank=True),
        ),
    ]
