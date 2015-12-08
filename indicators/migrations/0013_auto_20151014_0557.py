# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0020_auto_20151014_0557'),
        ('indicators', '0012_collecteddata_evidence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objective',
            options={'ordering': ('country', 'program', 'name')},
        ),
        migrations.AddField(
            model_name='objective',
            name='program',
            field=models.ForeignKey(blank=True, to='activitydb.Program', null=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='approval_submitted_by',
            field=models.ForeignKey(related_name='indicator_submitted_by', blank=True, to='activitydb.TolaUser', null=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='approved_by',
            field=models.ForeignKey(related_name='approving_indicator', blank=True, to='activitydb.TolaUser', null=True),
        ),
    ]
