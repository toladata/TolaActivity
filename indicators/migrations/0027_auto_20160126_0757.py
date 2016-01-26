# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0026_auto_20160125_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='program',
            field=models.ManyToManyField(to='activitydb.Program'),
        ),
    ]
