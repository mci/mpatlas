# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import django.contrib.gis.db.models.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('mpa', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name=b'Campaign id', serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=254, verbose_name=b'Name')),
                ('slug', models.SlugField(unique=True, max_length=254, blank=True)),
                ('country', models.CharField(max_length=20, verbose_name=b'Country / Territory')),
                ('sub_location', models.CharField(max_length=100, null=True, verbose_name=b'Sub Location', blank=True)),
                ('summary', ckeditor.fields.RichTextField(null=True, verbose_name=b'Campaign Description', blank=True)),
                ('point_geom', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('categories', taggit.managers.TaggableManager(to='category.Category', through='category.TaggedItem', blank=True, help_text=b'You can assign this area to one or more categories by providing a comma-separated list of tags (e.g., [ Shark Sanctuary, World Heritage Site ]', verbose_name=b'Categories')),
                ('mpas', models.ManyToManyField(to='mpa.Mpa', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Initiative',
            fields=[
                ('id', models.AutoField(verbose_name=b'Initiative id', serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=254, verbose_name=b'Name')),
                ('slug', models.SlugField(unique=True, max_length=254, blank=True)),
                ('summary', ckeditor.fields.RichTextField(null=True, verbose_name=b'Initiative Description', blank=True)),
                ('campaigns', models.ManyToManyField(to='campaign.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
