# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-11 03:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20160410_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personorganization',
            name='skills',
        ),
    ]
