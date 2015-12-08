# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0043_auto_20151102_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='approval',
            field=models.CharField(default='in progress', max_length=255, null=True, verbose_name='Approval', blank=True),
        ),
    ]
