# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-22 04:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rapp', '0008_auto_20170420_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='FireAlarm',
            fields=[
                ('room_number', models.TextField(max_length=10)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('occurence_time', models.TimeField()),
                ('specific_location', models.TextField(max_length=50)),
                ('fire_explanation', models.TextField(blank=True, help_text='If there was an actual fire, please explain here', max_length=200)),
                ('notes', models.TextField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProgramPacket',
            fields=[
                ('room_number', models.TextField(max_length=10)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('program_title', models.TextField(max_length=100)),
                ('program_date', models.DateField()),
                ('program_time', models.TimeField()),
                ('location1', models.TextField(max_length=50)),
                ('space_need_reservation1', models.BooleanField()),
                ('reservation_made1', models.BooleanField()),
                ('location2', models.TextField(max_length=50)),
                ('space_need_reservation2', models.BooleanField()),
                ('reservation_made2', models.BooleanField()),
                ('target_audience', models.TextField(max_length=200)),
                ('advertising', models.TextField(max_length=200)),
                ('coordinator_approval', models.BooleanField()),
                ('coordinator_sig', models.FileField(upload_to='')),
                ('sig_date', models.DateField()),
                ('program_description', models.TextField(max_length=500)),
                ('supplies', models.TextField(max_length=300)),
                ('proposed_cost', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SafetyInspectionViolation',
            fields=[
                ('room_number', models.TextField(max_length=10)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('prohibited_appliances', models.BooleanField(default=False)),
                ('candle_incense', models.BooleanField(default=False)),
                ('extension_cords', models.BooleanField(default=False)),
                ('lounge_furniture', models.BooleanField(default=False)),
                ('trash_violation', models.BooleanField(default=False)),
                ('animals', models.BooleanField(default=False)),
                ('alcohol_drugs', models.BooleanField(default=False)),
                ('fire_safety', models.BooleanField(default=False)),
                ('other', models.TextField(blank=True, max_length=200)),
                ('sig', models.FileField(upload_to='')),
                ('additional_action', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='ra',
            name='emergency_contact_phone',
            field=models.PositiveIntegerField(blank=True, default='1234567890'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='emergency_contact_phone',
            field=models.PositiveIntegerField(blank=True, default='1234567890'),
        ),
        migrations.AddField(
            model_name='safetyinspectionviolation',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapp.RA'),
        ),
        migrations.AddField(
            model_name='safetyinspectionviolation',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapp.ResidenceHall'),
        ),
        migrations.AddField(
            model_name='programpacket',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapp.RA'),
        ),
        migrations.AddField(
            model_name='programpacket',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapp.ResidenceHall'),
        ),
        migrations.AddField(
            model_name='firealarm',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapp.RA'),
        ),
        migrations.AddField(
            model_name='firealarm',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapp.ResidenceHall'),
        ),
        migrations.AddField(
            model_name='firealarm',
            name='other_ras',
            field=models.ManyToManyField(null=True, related_name='otherRAs', to='rapp.RA'),
        ),
    ]