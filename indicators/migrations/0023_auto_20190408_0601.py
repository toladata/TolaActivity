# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-08 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def load_frequencies(apps, schema_editor):
    frequency = apps.get_model("indicators", "Frequency")
    quaterly = frequency(id=100, frequency='Quaterly')
    quaterly.save()
    monthly = frequency(id=101, frequency='Monthly')
    monthly.save()
    annually = frequency(id=102, frequency='Annually')
    annually.save()
    baseline_endline = frequency(id=103, frequency='Baseline, Endline')
    baseline_endline.save()
    weekly = frequency(id=104, frequency='Weekly')
    weekly.save()
    baseline_midline_endline = frequency(id=105, frequency='Baseline, Midline, Endline')
    baseline_midline_endline.save()
    biweekly = frequency(id=106, frequency='Bi-weekly')
    biweekly.save()
    monthly_quaterly_annually = frequency(id=107, frequency='Monthly, Quaterly, Annually')
    monthly_quaterly_annually.save()
    end_of_cycle = frequency(id=108, frequency='End of cycle')
    end_of_cycle.save()


def delete_frequencies(apps, schema_editor):
    frequency = apps.get_model("indicators", "Frequency")
    frequency.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0022_auto_20190403_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequency',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow.Organization'),
        ),
        migrations.RunPython(load_frequencies, delete_frequencies),
    ]