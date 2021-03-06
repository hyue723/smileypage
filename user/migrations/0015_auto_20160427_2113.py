# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 01:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20160423_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='photo',
        ),
        migrations.AddField(
            model_name='profile',
            name='facebook_page',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_background',
            field=models.FileField(blank=True, default='/static/img/bg7.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_photo',
            field=models.FileField(blank=True, default='/static/img/smiley_face.png', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='status_in_cmu',
            field=models.CharField(choices=[('undergraduate', 'undergraduate student'), ('graduate', 'graduate student'), ('staff', 'school staff'), ('non_cmu', 'Not in CMU'), ('professor', 'professor')], default='undergraduate', max_length=2),
        ),
        migrations.AddField(
            model_name='profile',
            name='studying_fields',
            field=models.CharField(default=datetime.datetime(2016, 4, 28, 1, 13, 31, 244359, tzinfo=utc), max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.DurationField(),
        ),
    ]
