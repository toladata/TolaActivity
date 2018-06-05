# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-14 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formlibrary', '0008_customform_is_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customform',
            name='status',
            field=models.CharField(blank=True, choices=[('archived', 'Archived'), ('new', 'New'), ('published', 'Published'), ('unpublished', 'Unpublished')], default='new', max_length=15, null=True),
        ),
    ]