# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'EezMembership.area_in_eez'
        db.alter_column('spatialdata_eezmembership', 'area_in_eez', self.gf('django.db.models.fields.FloatField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'EezMembership.area_in_eez'
        db.alter_column('spatialdata_eezmembership', 'area_in_eez', self.gf('django.db.models.fields.FloatField')(default=0))


    models = {
        'spatialdata.eez': {
            'Meta': {'object_name': 'Eez'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eez': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'eez_id': ('django.db.models.fields.IntegerField', [], {}),
            'gazid': ('django.db.models.fields.FloatField', [], {}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '900913', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_3digit': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mpas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['wdpa.WdpaPolygon']", 'through': "orm['spatialdata.EezMembership']", 'symmetrical': 'False'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '900913', 'null': 'True'}),
            'sov_id': ('django.db.models.fields.IntegerField', [], {}),
            'sovereign': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'spatialdata.eezmembership': {
            'Meta': {'object_name': 'EezMembership'},
            'area_in_eez': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eez': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spatialdata.Eez']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wdpa.WdpaPolygon']"})
        },
        'spatialdata.eezsimplified': {
            'Meta': {'object_name': 'EezSimplified'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eez': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'eez_id': ('django.db.models.fields.IntegerField', [], {}),
            'gazid': ('django.db.models.fields.FloatField', [], {}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '900913', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_3digit': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'sov_id': ('django.db.models.fields.IntegerField', [], {}),
            'sovereign': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['spatialdata']
