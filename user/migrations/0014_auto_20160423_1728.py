# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.DateField(),
        ),
    ]