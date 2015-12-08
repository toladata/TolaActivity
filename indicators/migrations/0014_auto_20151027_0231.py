# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0013_auto_20151014_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='StrategicObjective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=135, blank=True)),
                ('description', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('country', models.ForeignKey(blank=True, to='activitydb.Country', null=True)),
            ],
            options={
                'ordering': ('country', 'name'),
            },
        ),
        migrations.AlterModelOptions(
            name='objective',
            options={'ordering': ('program', 'name')},
        ),
        migrations.RemoveField(
            model_name='objective',
            name='country',
        ),
        migrations.AlterField(
            model_name='indicator',
            name='objectives',
            field=models.ManyToManyField(related_name='obj_indicator', to='indicators.Objective', blank=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='strategic_objectives',
            field=models.ManyToManyField(related_name='strat_indicator', to='indicators.StrategicObjective', blank=True),
        ),
    ]
