# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 11:33
from __future__ import unicode_literals

import ckeditor.fields
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):
    
    initial = True

    dependencies = [
        ('mpa', '0001_squashed_0006_auto_20171106_2135'),
        ('category', '0001_squashed_0002_auto_20171106_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name=b'Campaign id')),
                ('name', models.CharField(max_length=254, verbose_name=b'Name')),
                ('slug', models.SlugField(blank=True, max_length=254, unique=True)),
                ('country', models.CharField(max_length=20, verbose_name=b'Country / Territory')),
                ('sub_location', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Sub Location')),
                ('summary', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name=b'Campaign Description')),
                ('point_geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('categories', taggit.managers.TaggableManager(blank=True, help_text=b'You can assign this area to one or more categories by providing a comma-separated list of tags (e.g., [ Shark Sanctuary, World Heritage Site ]', through='category.TaggedItem', to='category.Category', verbose_name=b'Categories')),
                ('mpas', models.ManyToManyField(blank=True, null=True, to='mpa.Mpa')),
            ],
        ),
        migrations.CreateModel(
            name='Initiative',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='Initiative id')),
                ('name', models.CharField(max_length=254, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, max_length=254, unique=True)),
                ('summary', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Initiative Description')),
                ('campaigns', models.ManyToManyField(to='campaign.Campaign')),
            ],
        ),
        migrations.AlterField(
            model_name='campaign',
            name='mpas',
            field=models.ManyToManyField(blank=True, to='mpa.Mpa'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='categories',
            field=taggit.managers.TaggableManager(blank=True, help_text='You can assign this area to one or more categories by providing a comma-separated list of tags (e.g., [ Shark Sanctuary, World Heritage Site ]', through='category.TaggedItem', to='category.Category', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='country',
            field=models.CharField(max_length=20, verbose_name='Country / Territory'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='Campaign id'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(max_length=254, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sub_location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Sub Location'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='summary',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Campaign Description'),
        ),
    ]