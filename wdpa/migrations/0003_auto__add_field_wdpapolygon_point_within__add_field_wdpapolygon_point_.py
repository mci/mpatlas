# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WdpaPolygon.point_within'
        db.add_column(u'wdpa_wdpapolygon', 'point_within',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(null=True),
                      keep_default=False)

        # Adding field 'WdpaPolygon.point_within_geojson'
        db.add_column(u'wdpa_wdpapolygon', 'point_within_geojson',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'WdpaPolygon.bbox'
        db.add_column(u'wdpa_wdpapolygon', 'bbox',
                      self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True),
                      keep_default=False)

        # Adding field 'WdpaPolygon.bbox_geojson'
        db.add_column(u'wdpa_wdpapolygon', 'bbox_geojson',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


        # Changing field 'WdpaPolygon.gis_area'
        db.alter_column(u'wdpa_wdpapolygon', 'gis_area', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WdpaPolygon.gis_m_area'
        db.alter_column(u'wdpa_wdpapolygon', 'gis_m_area', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WdpaPolygon.geog'
        db.alter_column(u'wdpa_wdpapolygon', 'geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, geography=True))

        # Changing field 'WdpaPolygon.status_yr'
        db.alter_column(u'wdpa_wdpapolygon', 'status_yr', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'WdpaPolygon.rep_m_area'
        db.alter_column(u'wdpa_wdpapolygon', 'rep_m_area', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WdpaPolygon.rep_area'
        db.alter_column(u'wdpa_wdpapolygon', 'rep_area', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WdpaPoint.geog'
        db.alter_column(u'wdpa_wdpapoint', 'geog', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True, geography=True))

        # Changing field 'WdpaPoint.status_yr'
        db.alter_column(u'wdpa_wdpapoint', 'status_yr', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'WdpaPoint.rep_m_area'
        db.alter_column(u'wdpa_wdpapoint', 'rep_m_area', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WdpaPoint.rep_area'
        db.alter_column(u'wdpa_wdpapoint', 'rep_area', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):
        # Deleting field 'WdpaPolygon.point_within'
        db.delete_column(u'wdpa_wdpapolygon', 'point_within')

        # Deleting field 'WdpaPolygon.point_within_geojson'
        db.delete_column(u'wdpa_wdpapolygon', 'point_within_geojson')

        # Deleting field 'WdpaPolygon.bbox'
        db.delete_column(u'wdpa_wdpapolygon', 'bbox')

        # Deleting field 'WdpaPolygon.bbox_geojson'
        db.delete_column(u'wdpa_wdpapolygon', 'bbox_geojson')


        # Changing field 'WdpaPolygon.gis_area'
        db.alter_column(u'wdpa_wdpapolygon', 'gis_area', self.gf('django.db.models.fields.FloatField')(default=None))

        # Changing field 'WdpaPolygon.gis_m_area'
        db.alter_column(u'wdpa_wdpapolygon', 'gis_m_area', self.gf('django.db.models.fields.FloatField')(default=None))

        # Changing field 'WdpaPolygon.geog'
        db.alter_column(u'wdpa_wdpapolygon', 'geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True))

        # Changing field 'WdpaPolygon.status_yr'
        db.alter_column(u'wdpa_wdpapolygon', 'status_yr', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'WdpaPolygon.rep_m_area'
        db.alter_column(u'wdpa_wdpapolygon', 'rep_m_area', self.gf('django.db.models.fields.FloatField')(default=None))

        # Changing field 'WdpaPolygon.rep_area'
        db.alter_column(u'wdpa_wdpapolygon', 'rep_area', self.gf('django.db.models.fields.FloatField')(default=None))

        # Changing field 'WdpaPoint.geog'
        db.alter_column(u'wdpa_wdpapoint', 'geog', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True))

        # Changing field 'WdpaPoint.status_yr'
        db.alter_column(u'wdpa_wdpapoint', 'status_yr', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'WdpaPoint.rep_m_area'
        db.alter_column(u'wdpa_wdpapoint', 'rep_m_area', self.gf('django.db.models.fields.FloatField')(default=None))

        # Changing field 'WdpaPoint.rep_area'
        db.alter_column(u'wdpa_wdpapoint', 'rep_area', self.gf('django.db.models.fields.FloatField')(default=None))

    models = {
        u'wdpa.wdpapoint': {
            'Meta': {'object_name': 'WdpaPoint'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'desig': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_eng': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'srid': '900913', 'null': 'True'}),
            'gov_type': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_crit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'iucn_cat': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mang_auth': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'mang_plan': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'marine': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'metadataid': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'orig_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'rep_area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rep_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status_yr': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sub_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wdpa_pid': ('django.db.models.fields.IntegerField', [], {}),
            'wdpaid': ('django.db.models.fields.IntegerField', [], {})
        },
        u'wdpa.wdpapolygon': {
            'Meta': {'object_name': 'WdpaPolygon'},
            'area_notes': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'bbox': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True'}),
            'bbox_geojson': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'desig': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_eng': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'difference': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '900913', 'null': 'True'}),
            'gis_area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gis_area_2': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'gis_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'gov_type': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_crit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'iucn_cat': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mang_auth': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'mang_plan': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'marine': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'metadataid': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'orig_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'point_within': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'point_within_geojson': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'rep_area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rep_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'shape_area': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status_yr': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sub_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wdpa_pid': ('django.db.models.fields.IntegerField', [], {}),
            'wdpaid': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['wdpa']