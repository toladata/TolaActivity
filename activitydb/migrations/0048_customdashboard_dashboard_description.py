# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0047_auto_20151119_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='customdashboard',
            name='dashboard_description',
            field=models.TextField(help_text='What does this custom dashboard displays to the user?', null=True, verbose_name='Brief Description', blank=True),
        ),
    ]
