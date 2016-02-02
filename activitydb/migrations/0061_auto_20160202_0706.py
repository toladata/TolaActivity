# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0060_auto_20160125_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='admin_level_three',
            field=models.ForeignKey(verbose_name='Administrative Level 3', blank=True, to='activitydb.AdminLevelThree', null=True),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='village',
            field=models.CharField(max_length=255, null=True, verbose_name='Administrative Level 4', blank=True),
        ),
    ]
