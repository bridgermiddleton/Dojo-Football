# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-23 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0002_auto_20191023_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='pweek',
            name='week',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tweek',
            name='week',
            field=models.IntegerField(default=7),
            preserve_default=False,
        ),
    ]
