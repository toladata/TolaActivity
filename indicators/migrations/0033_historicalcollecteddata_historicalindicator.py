# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0071_historicalbudget_historicalprojectagreement_historicalprojectcomplete_historicalsiteprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indicators', '0032_remove_indicator_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCollectedData',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('targeted', models.IntegerField(null=True, verbose_name=b'Targeted', blank=True)),
                ('achieved', models.IntegerField(null=True, verbose_name=b'Achieved', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Remarks/comments', blank=True)),
                ('date_collected', models.DateTimeField(null=True, blank=True)),
                ('comment', models.TextField(max_length=255, null=True, verbose_name=b'Comment/Explanation', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('agreement', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.ProjectAgreement', null=True)),
                ('approved_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.TolaUser', null=True)),
                ('complete', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.ProjectComplete', null=True)),
                ('evidence', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.Documentation', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('indicator', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='indicators.Indicator', null=True)),
                ('program', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.Program', null=True)),
                ('tola_table', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='indicators.TolaTable', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical collected data',
            },
        ),
        migrations.CreateModel(
            name='HistoricalIndicator',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('number', models.CharField(max_length=255, null=True, blank=True)),
                ('source', models.CharField(max_length=255, null=True, blank=True)),
                ('definition', models.TextField(null=True, blank=True)),
                ('baseline', models.CharField(max_length=255, null=True, blank=True)),
                ('lop_target', models.CharField(max_length=255, null=True, verbose_name=b'LOP Target', blank=True)),
                ('means_of_verification', models.CharField(max_length=255, null=True, blank=True)),
                ('data_collection_method', models.CharField(max_length=255, null=True, blank=True)),
                ('responsible_person', models.CharField(max_length=255, null=True, blank=True)),
                ('method_of_analysis', models.CharField(max_length=255, null=True, blank=True)),
                ('information_use', models.CharField(max_length=255, null=True, blank=True)),
                ('comments', models.TextField(max_length=255, null=True, blank=True)),
                ('key_performance_indicator', models.BooleanField(default=False, verbose_name=b'Key Performance Indicator for this program?')),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('approval_submitted_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.TolaUser', null=True)),
                ('approved_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.TolaUser', null=True)),
                ('country', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.Country', null=True)),
                ('external_service_record', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='indicators.ExternalServiceRecord', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('reporting_frequency', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='indicators.ReportingFrequency', null=True)),
                ('sector', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='activitydb.Sector', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical indicator',
            },
        ),
    ]
