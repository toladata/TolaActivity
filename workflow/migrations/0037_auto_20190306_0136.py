# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-06 09:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0036_merge_20190226_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='workflowlevel2',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
