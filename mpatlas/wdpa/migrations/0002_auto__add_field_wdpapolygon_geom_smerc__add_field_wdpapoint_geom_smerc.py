# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'WdpaPolygon.geom_smerc'
        db.add_column('wdpa_wdpapolygon', 'geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=900913, null=True), keep_default=False)

        # Adding field 'WdpaPoint.geom_smerc'
        db.add_column('wdpa_wdpapoint', 'geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(srid=900913, null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'WdpaPolygon.geom_smerc'
        db.delete_column('wdpa_wdpapolygon', 'geom_smerc')

        # Deleting field 'WdpaPoint.geom_smerc'
        db.delete_column('wdpa_wdpapoint', 'geom_smerc')


    models = {
        'wdpa.wdpapoint': {
            'Meta': {'object_name': 'WdpaPoint'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'desig': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_eng': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'srid': '900913', 'null': 'True'}),
            'gov_type': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_crit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'iucn_cat': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mang_auth': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'mang_plan': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'marine': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'metadataid': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'orig_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'rep_area': ('django.db.models.fields.FloatField', [], {}),
            'rep_m_area': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status_yr': ('django.db.models.fields.IntegerField', [], {}),
            'sub_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wdpa_pid': ('django.db.models.fields.IntegerField', [], {}),
            'wdpaid': ('django.db.models.fields.IntegerField', [], {})
        },
        'wdpa.wdpapolygon': {
            'Meta': {'object_name': 'WdpaPolygon'},
            'area_notes': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'desig': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_eng': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'difference': ('django.db.models.fields.FloatField', [], {}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '900913', 'null': 'True'}),
            'gis_area': ('django.db.models.fields.FloatField', [], {}),
            'gis_area_2': ('django.db.models.fields.FloatField', [], {}),
            'gis_m_area': ('django.db.models.fields.FloatField', [], {}),
            'gov_type': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'int_crit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'iucn_cat': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mang_auth': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'mang_plan': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'marine': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'metadataid': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'orig_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'rep_area': ('django.db.models.fields.FloatField', [], {}),
            'rep_m_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_area': ('django.db.models.fields.FloatField', [], {}),
            'shape_leng': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status_yr': ('django.db.models.fields.IntegerField', [], {}),
            'sub_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wdpa_pid': ('django.db.models.fields.IntegerField', [], {}),
            'wdpaid': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['wdpa']
