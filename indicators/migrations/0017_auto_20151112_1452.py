# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0016_auto_20151106_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('url', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExternalServiceRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_url', models.CharField(max_length=765, blank=True)),
                ('record_id', models.CharField(max_length=765, verbose_name=b'Unique ID', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('external_service', models.ForeignKey(blank=True, to='indicators.ExternalService', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='indicator',
            name='external_service_record',
            field=models.ForeignKey(blank=True, to='indicators.ExternalServiceRecord', null=True),
        ),
    ]
