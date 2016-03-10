# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0031_auto_20160216_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='owner',
        ),
    ]
