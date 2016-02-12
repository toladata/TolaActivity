# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0063_auto_20160211_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='village',
            name='admin_3',
            field=models.ForeignKey(blank=True, to='activitydb.AdminLevelThree', null=True),
        ),
        migrations.AlterField(
            model_name='village',
            name='district',
            field=models.ForeignKey(blank=True, to='activitydb.District', null=True),
        ),
    ]
