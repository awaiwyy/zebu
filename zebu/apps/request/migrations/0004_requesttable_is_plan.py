# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-17 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_auto_20160316_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesttable',
            name='is_plan',
            field=models.BooleanField(default=False),
        ),
    ]
