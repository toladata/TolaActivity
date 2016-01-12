# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0052_auto_20151210_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='program',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_budget',
            field=models.DecimalField(default=Decimal('0.00'), help_text='What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit', verbose_name='Actual Cost', max_digits=20, decimal_places=2),
        ),
    ]
