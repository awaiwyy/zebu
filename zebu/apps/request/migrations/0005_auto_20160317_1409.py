# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-17 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_requesttable_is_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requesttable',
            name='is_plan',
            field=models.NullBooleanField(default='No'),
        ),
    ]
