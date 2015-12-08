# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0010_auto_20150929_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='achieved',
            field=models.IntegerField(null=True, verbose_name=b'Achieved', blank=True),
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='targeted',
            field=models.IntegerField(null=True, verbose_name=b'Targeted', blank=True),
        ),
    ]
