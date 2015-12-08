# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0036_auto_20151028_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteprofile',
            name='avg_landholding_size',
            field=models.DecimalField(decimal_places=14, max_digits=25, blank=True, help_text='In hectares/jeribs', null=True, verbose_name='Average Landholding Size'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='populations_owning_land',
            field=models.IntegerField(help_text='(%)', null=True, verbose_name='Households Owning Land', blank=True),
        ),

        migrations.AlterField(
            model_name='siteprofile',
            name='literacy_rate',
            field=models.IntegerField(help_text='%', null=True, verbose_name='Literacy Rate (%)', blank=True),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='literate_females',
            field=models.IntegerField(help_text='%', null=True, verbose_name='% of Literate Females', blank=True),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='literate_males',
            field=models.IntegerField(help_text='%', null=True, verbose_name='% of Literate Males', blank=True),
        ),
    ]
