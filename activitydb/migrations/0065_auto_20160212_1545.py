# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0064_auto_20160211_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='stakeholder',
            name='approval',
            field=models.CharField(default='in progress', max_length=255, null=True, verbose_name='Approval', blank=True),
        ),
        migrations.AddField(
            model_name='stakeholder',
            name='approved_by',
            field=models.ForeignKey(related_name='stake_approving', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AddField(
            model_name='stakeholder',
            name='filled_by',
            field=models.ForeignKey(related_name='stake_filled', blank=True, to='activitydb.TolaUser', null=True),
        ),
    ]
