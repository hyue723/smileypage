# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 04:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20160418_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='user',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sex',
        ),
    ]
