# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0020_auto_20151014_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLevelThree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='District Name', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('district', models.ForeignKey(to='activitydb.District')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
