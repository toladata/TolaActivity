# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-05-22 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beneficiary_name', models.CharField(blank=True, max_length=255, null=True)),
                ('father_name', models.CharField(blank=True, max_length=255, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=255, null=True)),
                ('signature', models.BooleanField(default=True)),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('edit_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('beneficiary_name',),
            },
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distribution_name', models.CharField(max_length=255)),
                ('distribution_indicator', models.CharField(max_length=255)),
                ('distribution_implementer', models.CharField(blank=True, max_length=255, null=True)),
                ('reporting_period', models.CharField(blank=True, max_length=255, null=True)),
                ('total_beneficiaries_received_input', models.IntegerField(blank=True, null=True)),
                ('distribution_location', models.CharField(blank=True, max_length=255, null=True)),
                ('input_type_distributed', models.CharField(blank=True, max_length=255, null=True)),
                ('distributor_name_and_affiliation', models.CharField(blank=True, max_length=255, null=True)),
                ('distributor_contact_number', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('form_filled_by', models.CharField(blank=True, max_length=255, null=True)),
                ('form_filled_by_position', models.CharField(blank=True, max_length=255, null=True)),
                ('form_filled_by_contact_num', models.CharField(blank=True, max_length=255, null=True)),
                ('form_filled_date', models.CharField(blank=True, max_length=255, null=True)),
                ('form_verified_by', models.CharField(blank=True, max_length=255, null=True)),
                ('form_verified_by_position', models.CharField(blank=True, max_length=255, null=True)),
                ('form_verified_by_contact_num', models.CharField(blank=True, max_length=255, null=True)),
                ('form_verified_date', models.CharField(blank=True, max_length=255, null=True)),
                ('total_received_input', models.CharField(blank=True, max_length=255, null=True)),
                ('total_male', models.IntegerField(blank=True, null=True)),
                ('total_female', models.IntegerField(blank=True, null=True)),
                ('total_age_0_14_male', models.IntegerField(blank=True, null=True)),
                ('total_age_0_14_female', models.IntegerField(blank=True, null=True)),
                ('total_age_15_24_male', models.IntegerField(blank=True, null=True)),
                ('total_age_15_24_female', models.IntegerField(blank=True, null=True)),
                ('total_age_25_59_male', models.IntegerField(blank=True, null=True)),
                ('total_age_25_59_female', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('edit_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('distribution_name',),
            },
        ),
        migrations.CreateModel(
            name='TrainingAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_name', models.CharField(max_length=255)),
                ('implementer', models.CharField(blank=True, max_length=255, null=True)),
                ('reporting_period', models.CharField(blank=True, max_length=255, null=True)),
                ('total_participants', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('community', models.CharField(blank=True, max_length=255, null=True)),
                ('training_duration', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.CharField(blank=True, max_length=255, null=True)),
                ('end_date', models.CharField(blank=True, max_length=255, null=True)),
                ('trainer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('trainer_contact_num', models.CharField(blank=True, max_length=255, null=True)),
                ('form_filled_by', models.CharField(blank=True, max_length=255, null=True)),
                ('form_filled_by_contact_num', models.CharField(blank=True, max_length=255, null=True)),
                ('total_male', models.IntegerField(blank=True, null=True)),
                ('total_female', models.IntegerField(blank=True, null=True)),
                ('total_age_0_14_male', models.IntegerField(blank=True, null=True)),
                ('total_age_0_14_female', models.IntegerField(blank=True, null=True)),
                ('total_age_15_24_male', models.IntegerField(blank=True, null=True)),
                ('total_age_15_24_female', models.IntegerField(blank=True, null=True)),
                ('total_age_25_59_male', models.IntegerField(blank=True, null=True)),
                ('total_age_25_59_female', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('edit_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('training_name',),
            },
        ),
    ]
