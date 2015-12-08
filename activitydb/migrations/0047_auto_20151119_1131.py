# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0046_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitem',
            name='item',
            field=models.CharField(default='Unnamed Item', max_length=255),
            preserve_default=False,
        ),
    ]
