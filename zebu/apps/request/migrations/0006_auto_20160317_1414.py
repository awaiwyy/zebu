# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-17 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0005_auto_20160317_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requesttable',
            name='is_plan',
            field=models.CharField(default='false', max_length=20),
        ),
    ]
