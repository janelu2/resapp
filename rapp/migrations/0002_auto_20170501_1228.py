# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 18:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 1, 22, 28, 13, 900168, tzinfo=utc)),
        ),
    ]
