# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 16:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default=datetime.datetime(2016, 4, 14, 16, 20, 57, 624230, tzinfo=utc), max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default=datetime.datetime(2016, 4, 14, 16, 21, 5, 261083, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
