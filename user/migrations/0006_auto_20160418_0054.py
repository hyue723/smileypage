# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 04:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20160418_0049'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=200)),
                ('sex', models.CharField(default='Unknown', max_length=10)),
                ('age', models.CharField(default='Unknown', max_length=10)),
                ('birthdate', models.CharField(default='Unknown', max_length=20)),
                ('interests', models.CharField(default='Unknown', max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
