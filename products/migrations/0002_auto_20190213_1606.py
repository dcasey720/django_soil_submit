# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-13 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='elements_determined',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='product',
            name='purpose',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='product',
            name='test',
            field=models.CharField(default='', max_length=254),
        ),
    ]