# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0023_auto_20151022_0500'),
    ]

    operations = [
        migrations.RenameModel('Community','SiteProfile'),
        migrations.AlterModelOptions(
            name='stakeholdertype',
            options={'ordering': ('name',), 'verbose_name_plural': 'Stakeholder Types'},
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='global_item',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='community',
            field=models.ForeignKey(blank=True, to='activitydb.SiteProfile', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='community',
            field=models.ManyToManyField(to='activitydb.SiteProfile', blank=True),
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='stakeholder',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='stakeholder',
            field=models.ManyToManyField(to='activitydb.Stakeholder', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='community',
            field=models.ManyToManyField(to='activitydb.SiteProfile', blank=True),
        ),
    ]
