# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0026_auto_20151026_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='in_file',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='not_applicable',
            field=models.BooleanField(default=False),
        ),
    ]
