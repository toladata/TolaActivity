# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-07 14:02
from __future__ import unicode_literals

from django.db import migrations
from ..models import CustomForm


def set_form_public(apps, schema_editor):
    CustomForm.objects.filter(is_public=True).update(
        public={'org': True, 'url': False})


class Migration(migrations.Migration):

    dependencies = [
        ('formlibrary', '0013_auto_20180807_0436'),
    ]

    operations = [
        migrations.RunPython(set_form_public),
    ]
