# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0069_program_user_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='tolauser',
            name='tables_api_token',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
