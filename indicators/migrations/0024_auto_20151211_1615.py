# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indicators', '0023_collecteddata_table_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='TolaTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('table_id', models.IntegerField(null=True, blank=True)),
                ('remote_owner', models.CharField(max_length=255, blank=True)),
                ('url', models.CharField(max_length=255, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='table_link',
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='tola_table',
            field=models.ForeignKey(blank=True, to='indicators.TolaTable', null=True),
        ),
    ]
