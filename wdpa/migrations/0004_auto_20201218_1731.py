# Generated by Django 2.2.15 on 2020-12-18 17:31

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wdpa', '0003_wdpa2019point_wdpa2019poly'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wdpa2020Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wdpaid', models.FloatField()),
                ('wdpa_pid', models.CharField(blank=True, max_length=52)),
                ('pa_def', models.CharField(blank=True, max_length=20)),
                ('name', models.CharField(blank=True, max_length=254)),
                ('orig_name', models.CharField(blank=True, max_length=254)),
                ('desig', models.CharField(blank=True, max_length=254)),
                ('desig_eng', models.CharField(blank=True, max_length=254)),
                ('desig_type', models.CharField(blank=True, max_length=20)),
                ('iucn_cat', models.CharField(blank=True, max_length=20)),
                ('int_crit', models.CharField(blank=True, max_length=100)),
                ('marine', models.CharField(blank=True, max_length=20)),
                ('no_take', models.CharField(blank=True, max_length=50)),
                ('no_tk_area', models.FloatField(null=True)),
                ('rep_m_area', models.FloatField(null=True)),
                ('rep_area', models.FloatField(null=True)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('status_yr', models.IntegerField(null=True)),
                ('gov_type', models.CharField(blank=True, max_length=254)),
                ('own_type', models.CharField(blank=True, max_length=254)),
                ('mang_auth', models.CharField(blank=True, max_length=254)),
                ('mang_plan', models.CharField(blank=True, max_length=254)),
                ('parent_iso3', models.CharField(blank=True, max_length=50)),
                ('iso3', models.CharField(max_length=50)),
                ('sub_loc', models.CharField(blank=True, max_length=100)),
                ('verif', models.CharField(blank=True, max_length=20)),
                ('metadataid', models.IntegerField()),
                ('supp_info', models.CharField(blank=True, max_length=254)),
                ('cons_obj', models.CharField(blank=True, max_length=100)),
                ('gis_area', models.FloatField(null=True)),
                ('gis_m_area', models.FloatField(null=True)),
                ('shape_length', models.FloatField(default=0)),
                ('shape_area', models.FloatField(default=0)),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wdpa2020Poly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wdpaid', models.FloatField()),
                ('wdpa_pid', models.CharField(blank=True, max_length=52)),
                ('pa_def', models.CharField(blank=True, max_length=20)),
                ('name', models.CharField(blank=True, max_length=254)),
                ('orig_name', models.CharField(blank=True, max_length=254)),
                ('desig', models.CharField(blank=True, max_length=254)),
                ('desig_eng', models.CharField(blank=True, max_length=254)),
                ('desig_type', models.CharField(blank=True, max_length=20)),
                ('iucn_cat', models.CharField(blank=True, max_length=20)),
                ('int_crit', models.CharField(blank=True, max_length=100)),
                ('marine', models.CharField(blank=True, max_length=20)),
                ('no_take', models.CharField(blank=True, max_length=50)),
                ('no_tk_area', models.FloatField(null=True)),
                ('rep_m_area', models.FloatField(null=True)),
                ('rep_area', models.FloatField(null=True)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('status_yr', models.IntegerField(null=True)),
                ('gov_type', models.CharField(blank=True, max_length=254)),
                ('own_type', models.CharField(blank=True, max_length=254)),
                ('mang_auth', models.CharField(blank=True, max_length=254)),
                ('mang_plan', models.CharField(blank=True, max_length=254)),
                ('parent_iso3', models.CharField(blank=True, max_length=50)),
                ('iso3', models.CharField(max_length=50)),
                ('sub_loc', models.CharField(blank=True, max_length=100)),
                ('verif', models.CharField(blank=True, max_length=20)),
                ('metadataid', models.IntegerField()),
                ('supp_info', models.CharField(blank=True, max_length=254)),
                ('cons_obj', models.CharField(blank=True, max_length=100)),
                ('gis_area', models.FloatField(null=True)),
                ('gis_m_area', models.FloatField(null=True)),
                ('shape_length', models.FloatField(default=0)),
                ('shape_area', models.FloatField(default=0)),
                ('geom_smerc', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=900913)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('geog', django.contrib.gis.db.models.fields.MultiPolygonField(geography=True, null=True, srid=4326)),
                ('point_within', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('point_within_geojson', models.TextField(null=True)),
                ('bbox', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326)),
                ('bbox_geojson', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='wdpa2014point',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpa2014point',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='wdpa2014polygon',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpa2014polygon',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='wdpa2018point',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpa2018point',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='wdpa2018poly',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpa2018poly',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='wdpa2019point',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpa2019point',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='wdpa2019poly',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpa2019poly',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='wdpapoint',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpapoint',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='wdpapolygon',
            name='cons_obj',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wdpapolygon',
            name='supp_info',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
