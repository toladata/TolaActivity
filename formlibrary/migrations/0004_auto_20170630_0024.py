# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 07:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formlibrary', '0003_auto_20170522_0737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='distribution',
            old_name='initiation',
            new_name='workflowlevel2',
        ),
    ]
