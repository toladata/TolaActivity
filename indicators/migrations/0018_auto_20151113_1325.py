# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0017_auto_20151112_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='external_service_record',
            field=models.ForeignKey(verbose_name=b'External Service ID', blank=True, to='indicators.ExternalServiceRecord', null=True),
        ),
    ]
