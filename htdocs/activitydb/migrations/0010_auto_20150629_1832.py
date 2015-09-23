# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0009_auto_20150629_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='program',
            field=models.ForeignKey(related_name='agreement', to='activitydb.Program'),
        ),
    ]
