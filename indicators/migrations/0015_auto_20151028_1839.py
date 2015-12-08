# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0014_auto_20151027_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='evidence',
            field=models.ForeignKey(verbose_name=b'Evidence Document or Link', blank=True, to='activitydb.Documentation', null=True),
        ),
    ]
