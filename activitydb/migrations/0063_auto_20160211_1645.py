# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0062_auto_20160206_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='village',
            name='admin_3',
            field=models.ForeignKey(default=1, to='activitydb.AdminLevelThree'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tolauser',
            name='countries',
            field=models.ManyToManyField(related_name='countries', verbose_name='Accessible Countries', to='activitydb.Country', blank=True),
        ),
    ]
