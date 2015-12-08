# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0028_auto_20151027_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitem',
            name='global_item',
            field=models.BooleanField(default=False),
        ),
    ]
