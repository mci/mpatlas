# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 18:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpa', '0011_auto_20180920_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mpa',
            name='marine_old',
        ),
    ]