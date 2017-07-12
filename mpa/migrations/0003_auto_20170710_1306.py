# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 13:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('mpa', '0002_auto_20170213_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name=b'Data Source Name')),
                ('version', models.CharField(max_length=500, verbose_name=b'Version or Access Date')),
                ('url', models.URLField(blank=True, max_length=500, null=True, verbose_name=b'Data Source URL')),
                ('logo', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasource_logos', to='filer.Image')),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='logo',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_logos', to='filer.Image'),
        ),
    ]