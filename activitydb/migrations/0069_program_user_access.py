# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0068_auto_20160308_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='user_access',
            field=models.ManyToManyField(to='activitydb.TolaUser', blank=True),
        ),
    ]
