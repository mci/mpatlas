# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 11:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    replaces = [('accounts', '0001_initial'), ('accounts', '0002_auto_20171106_2137')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('--', ''), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Miss', 'Miss'), ('Dr', 'Dr')], default='', max_length=200)),
                ('affiliation', models.CharField(blank=True, max_length=300, verbose_name='organization')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
