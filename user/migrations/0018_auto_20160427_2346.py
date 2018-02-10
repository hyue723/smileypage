# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 03:46
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20160427_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='kind',
            field=models.CharField(choices=[('food', 'Food'), ('study', 'Study'), ('other', 'Other')], default='food', max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
