# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-26 12:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_auto_20160326_1205'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]
