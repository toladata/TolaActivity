# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0015_auto_20151028_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='definition',
            field=models.TextField(null=True, blank=True),
        ),
    ]
