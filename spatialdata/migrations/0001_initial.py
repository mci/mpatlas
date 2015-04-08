# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mpa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eez',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eez', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=100)),
                ('objectid', models.IntegerField()),
                ('sovereign', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=150)),
                ('sov_id', models.IntegerField()),
                ('iso_3digit', models.CharField(max_length=50)),
                ('gazid', models.FloatField()),
                ('eez_id', models.IntegerField()),
                ('area', models.FloatField()),
                ('geom_smerc', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('geog', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True)),
                ('simple_geom_smerc', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857, null=True)),
                ('simple_geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('simple_geog', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EezMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area_in_eez', models.FloatField(null=True, verbose_name=b'mpa area in eez (m2)')),
                ('eez', models.ForeignKey(to='spatialdata.Eez')),
                ('mpa', models.ForeignKey(to='mpa.Mpa')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ecoregion_code', models.FloatField()),
                ('ecoregion', models.CharField(max_length=50)),
                ('province_code', models.FloatField()),
                ('province', models.CharField(max_length=40)),
                ('realm_code', models.FloatField()),
                ('realm', models.CharField(max_length=40)),
                ('alt_code', models.FloatField()),
                ('ecoregion_code_x', models.FloatField()),
                ('latitude_zone', models.CharField(max_length=10)),
                ('geom_smerc', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('geog', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True)),
                ('simple_geom_smerc', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857, null=True)),
                ('simple_geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('simple_geog', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=240)),
                ('iso3code', models.CharField(default=b'', max_length=3)),
                ('summary', ckeditor.fields.RichTextField(null=True, verbose_name=b'Nation Protection Summary', blank=True)),
                ('marine_area', models.FloatField(null=True, blank=True)),
                ('mpa_area', models.FloatField(null=True, blank=True)),
                ('mpa_percent', models.FloatField(null=True, blank=True)),
                ('notake_area', models.FloatField(null=True, blank=True)),
                ('notake_percent', models.FloatField(null=True, blank=True)),
                ('geom_smerc', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('geog', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True)),
                ('simple_geom_smerc', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857, null=True)),
                ('simple_geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True)),
                ('simple_geog', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eez',
            name='mpas',
            field=models.ManyToManyField(to='mpa.Mpa', verbose_name=b'MPAs within this EEZ', through='spatialdata.EezMembership'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eez',
            name='nation',
            field=models.ForeignKey(default=None, to='spatialdata.Nation', null=True),
            preserve_default=True,
        ),
    ]
