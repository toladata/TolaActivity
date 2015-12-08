# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0024_auto_20151024_0040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='siteprofile',
            options={'ordering': ('name',), 'verbose_name_plural': 'Site Profiles'},
        ),
        migrations.RemoveField(
            model_name='stakeholdertype',
            name='country',
        ),
    ]
