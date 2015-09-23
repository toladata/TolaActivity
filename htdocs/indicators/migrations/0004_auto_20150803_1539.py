# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0014_auto_20150803_1539'),
        ('indicators', '0003_auto_20150701_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collecteddata',
            options={'ordering': ('agreement', 'indicator', 'date_collected', 'create_date'), 'verbose_name_plural': 'Indicator Output/Outcome Collected Data'},
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='analysis_name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Analysis Done By', blank=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='comment',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Comment/Explanation', blank=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='date_of_analysis',
            field=models.DateTimeField(null=True, verbose_name=b'Date of Analysis', blank=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='date_of_training',
            field=models.DateTimeField(null=True, verbose_name=b'Date of Staff Training', blank=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='method',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Method of Data Collection', blank=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='office',
            field=models.ForeignKey(related_name='q_office', blank=True, to='activitydb.Office', null=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='tool',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Tool/Source Developed By', blank=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='trainer_name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Name of Trainer', blank=True),
        ),
    ]
