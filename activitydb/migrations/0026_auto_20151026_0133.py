# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0025_auto_20151024_0221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectagreement',
            old_name='community',
            new_name='site',
        ),
        migrations.RenameField(
            model_name='projectcomplete',
            old_name='community',
            new_name='site',
        ),
    ]
