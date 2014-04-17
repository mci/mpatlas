# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WdpaPolygon'
        db.create_table('wdpa_wdpapolygon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('wdpaid', self.gf('django.db.models.fields.IntegerField')()),
            ('wdpa_pid', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('orig_name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sub_loc', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('desig', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('desig_eng', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('desig_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('iucn_cat', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('int_crit', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('marine', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('rep_m_area', self.gf('django.db.models.fields.FloatField')()),
            ('gis_m_area', self.gf('django.db.models.fields.FloatField')()),
            ('rep_area', self.gf('django.db.models.fields.FloatField')()),
            ('gis_area', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status_yr', self.gf('django.db.models.fields.IntegerField')()),
            ('gov_type', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('mang_auth', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('mang_plan', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('metadataid', self.gf('django.db.models.fields.IntegerField')()),
            ('area_notes', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('gis_area_2', self.gf('django.db.models.fields.FloatField')()),
            ('difference', self.gf('django.db.models.fields.FloatField')()),
            ('shape_leng', self.gf('django.db.models.fields.FloatField')()),
            ('shape_area', self.gf('django.db.models.fields.FloatField')()),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
            ('geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
        ))
        db.send_create_signal('wdpa', ['WdpaPolygon'])

        # Adding model 'WdpaPoint'
        db.create_table('wdpa_wdpapoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('wdpaid', self.gf('django.db.models.fields.IntegerField')()),
            ('wdpa_pid', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('orig_name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sub_loc', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('desig', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('desig_eng', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('desig_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('iucn_cat', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('int_crit', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('marine', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('rep_m_area', self.gf('django.db.models.fields.FloatField')()),
            ('rep_area', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status_yr', self.gf('django.db.models.fields.IntegerField')()),
            ('gov_type', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('mang_auth', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('mang_plan', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('metadataid', self.gf('django.db.models.fields.IntegerField')()),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True)),
            ('geog', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True)),
        ))
        db.send_create_signal('wdpa', ['WdpaPoint'])


    def backwards(self, orm):
        
        # Deleting model 'WdpaPolygon'
        db.delete_table('wdpa_wdpapolygon')

        # Deleting model 'WdpaPoint'
        db.delete_table('wdpa_wdpapoint')


    models = {
        'wdpa.wdpapoint': {
            'Meta': {'object_name': 'WdpaPoint'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'desig': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_eng': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'desig_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
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
