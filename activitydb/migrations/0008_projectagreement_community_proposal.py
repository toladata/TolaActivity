# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0007_auto_20150629_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='community_proposal',
            field=models.FileField(upload_to='uploads', null=True, verbose_name='Community Proposal', blank=True),
        ),
    ]
