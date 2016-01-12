# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0022_auto_20151209_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteddata',
            name='table_link',
            field=models.CharField(max_length=b'255', null=True, verbose_name=b'Tola Table', blank=True),
        ),
    ]
