# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 01:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20160420_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(default='', max_length=800),
        ),
    ]
