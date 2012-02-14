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

        # Adding model 'EezMembership'
        db.create_table('spatialdata_eezmembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eez', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spatialdata.Eez'])),
            ('mpa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mpa.Mpa'])),
            ('area_in_eez', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('spatialdata', ['EezMembership'])

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

        # Deleting model 'EezMembership'
        db.delete_table('spatialdata_eezmembership')

        # Deleting model 'EezSimplified'
        db.delete_table('spatialdata_eezsimplified')


    models = {
        'mpa.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'mpa.mpa': {
            'Meta': {'object_name': 'Mpa'},
            'access': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'access_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bbox_lowerleft': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'bbox_upperright': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'calc_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'calc_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'conservation_effectiveness': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'conservation_focus_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'constancy': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'constancy_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mpa_main_set'", 'null': 'True', 'to': "orm['mpa.Contact']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'designation_eng': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'designation_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fishing': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'fishing_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fishing_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'}),
            'gov_type': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'int_criteria': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_point': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'iucn_category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'marine': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'mgmt_auth': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'mgmt_plan_ref': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'mgmt_plan_type': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'mpa_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'no_take': ('django.db.models.fields.CharField', [], {'default': "'Not Reported'", 'max_length': '100'}),
            'no_take_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'other_contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mpa.Contact']", 'null': 'True', 'symmetrical': 'False'}),
            'permanence': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'permanence_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'point_geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'point_geom': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'point_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'srid': '3857', 'null': 'True'}),
            'point_within': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'primary_conservation_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'protection_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'protection_focus_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'protection_focus_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'protection_level': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'rep_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rep_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_conservation_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Designated'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sub_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tertiary_conservation_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'usmpa_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'wdpa_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wdpa_notes': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
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
            'mpas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mpa.Mpa']", 'through': "orm['spatialdata.EezMembership']", 'symmetrical': 'False'}),
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
            'mpa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mpa.Mpa']"})
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
