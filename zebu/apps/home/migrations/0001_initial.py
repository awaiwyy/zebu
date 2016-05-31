# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-15 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='scheduleInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sdate', models.DateField()),
                ('total', models.IntegerField()),
                ('used', models.IntegerField()),
                ('arrangement', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=50)),
            ],
        ),
    ]
