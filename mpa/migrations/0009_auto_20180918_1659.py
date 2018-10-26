# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-18 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mpa', '0008_auto_20180213_0214'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpa',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Date and time record created', verbose_name='Creation Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mpa',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, help_text='Date and time of last record save', verbose_name='Modification Date'),
        ),
    ]