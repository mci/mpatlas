# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Eez'
        db.create_table('spatialdata_eez', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eez', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('sovereign', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('sov_id', self.gf('django.db.models.fields.IntegerField')()),
            ('iso_3digit', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gazid', self.gf('django.db.models.fields.FloatField')()),
            ('eez_id', self.gf('django.db.models.fields.IntegerField')()),
            ('area', self.gf('django.db.models.fields.FloatField')()),
            ('geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=900913, null=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
            ('geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
            ('simple_geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=900913, null=True)),
            ('simple_geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
            ('simple_geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
        ))
        db.send_create_signal('spatialdata', ['Eez'])

        # Adding model 'EezSimplified'
        db.create_table('spatialdata_eezsimplified', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eez', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('sovereign', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('sov_id', self.gf('django.db.models.fields.IntegerField')()),
            ('iso_3digit', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gazid', self.gf('django.db.models.fields.FloatField')()),
            ('eez_id', self.gf('django.db.models.fields.IntegerField')()),
            ('area', self.gf('django.db.models.fields.FloatField')()),
            ('geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=900913, null=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
            ('geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True)),
        ))
        db.send_create_signal('spatialdata', ['EezSimplified'])


    def backwards(self, orm):
        
        # Deleting model 'Eez'
        db.delete_table('spatialdata_eez')

        # Deleting model 'EezSimplified'
        db.delete_table('spatialdata_eezsimplified')


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
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '900913', 'null': 'True'}),
            'sov_id': ('django.db.models.fields.IntegerField', [], {}),
            'sovereign': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        }
    }

    complete_apps = ['spatialdata']
