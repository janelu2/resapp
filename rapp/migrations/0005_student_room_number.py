# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapp', '0004_auto_20170318_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='room_number',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
