# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-19 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0011_auto_20190219_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='sample_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]