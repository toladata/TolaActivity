# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0029_auto_20160203_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='indicator',
            field=models.ForeignKey(default=1, to='indicators.Indicator'),
            preserve_default=False,
        ),
    ]
