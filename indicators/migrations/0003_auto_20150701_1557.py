# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0002_objective_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='description',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Remarks/comments', blank=True),
        ),
    ]
