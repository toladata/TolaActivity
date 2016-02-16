# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0065_auto_20160212_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tolauser',
            name='modified_by',
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='latitude',
            field=models.DecimalField(default=Decimal('0.00'), verbose_name='Latitude (Decimal Coordinates)', max_digits=25, decimal_places=16),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='longitude',
            field=models.DecimalField(default=Decimal('0.00'), verbose_name='Longitude (Decimal Coordinates)', max_digits=25, decimal_places=16),
        ),
    ]
