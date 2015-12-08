# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0020_collecteddata_approved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collecteddata',
            name='comment',
            field=models.TextField(max_length=255, null=True, verbose_name=b'Comment/Explanation', blank=True),
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Remarks/comments', blank=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='comments',
            field=models.TextField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='indicatortype',
            name='description',
            field=models.TextField(max_length=765, blank=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='description',
            field=models.TextField(max_length=765, blank=True),
        ),
        migrations.AlterField(
            model_name='objective',
            name='description',
            field=models.TextField(max_length=765, blank=True),
        ),
        migrations.AlterField(
            model_name='strategicobjective',
            name='description',
            field=models.TextField(max_length=765, blank=True),
        ),
    ]
