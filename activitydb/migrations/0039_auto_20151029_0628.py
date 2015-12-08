# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0038_auto_20151029_0616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteprofile',
            old_name='community_leader',
            new_name='contact_leader',
        ),
    ]
