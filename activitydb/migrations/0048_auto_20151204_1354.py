# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0047_auto_20151119_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiary',
            old_name='community',
            new_name='site',
        ),
        migrations.AlterField(
            model_name='country',
            name='description',
            field=models.TextField(max_length=765, verbose_name='Description/Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='description',
            field=models.TextField(max_length=765, null=True, verbose_name='Program Description', blank=True),
        ),
        migrations.AlterField(
            model_name='projecttype',
            name='description',
            field=models.CharField(max_length=765),
        ),
        migrations.AlterField(
            model_name='projecttypeother',
            name='description',
            field=models.CharField(max_length=765),
        ),
        migrations.AlterField(
            model_name='template',
            name='description',
            field=models.CharField(max_length=765),
        ),
    ]
