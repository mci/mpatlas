# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Nation.marine_area'
        db.add_column(u'spatialdata_nation', 'marine_area',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Nation.mpa_area'
        db.add_column(u'spatialdata_nation', 'mpa_area',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Nation.mpa_percent'
        db.add_column(u'spatialdata_nation', 'mpa_percent',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Nation.marine_area'
        db.delete_column(u'spatialdata_nation', 'marine_area')

        # Deleting field 'Nation.mpa_area'
        db.delete_column(u'spatialdata_nation', 'mpa_area')

        # Deleting field 'Nation.mpa_percent'
        db.delete_column(u'spatialdata_nation', 'mpa_percent')


    models = {
        u'mpa.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'mpa.mpa': {
            'Meta': {'object_name': 'Mpa'},
            'access': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'access_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bbox_lowerleft': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'bbox_upperright': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'calc_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'calc_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'conservation_effectiveness': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'conservation_focus_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'conservation_focus_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'constancy': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'constancy_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mpa_main_set'", 'null': 'True', 'to': u"orm['mpa.Contact']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'designation_eng': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'designation_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fishing': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'fishing_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fishing_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'gov_type': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'int_criteria': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_point': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'iucn_category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'marine': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'mgmt_auth': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'mgmt_plan_ref': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'mgmt_plan_type': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'mpa_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'no_take': ('django.db.models.fields.CharField', [], {'default': "'Not Reported'", 'max_length': '100'}),
            'no_take_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'other_contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['mpa.Contact']", 'null': 'True', 'blank': 'True'}),
            'other_ids': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'permanence': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'permanence_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'point_geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'point_geom': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True', 'blank': 'True'}),
            'point_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'point_within': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'primary_conservation_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'protection_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'protection_focus_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'protection_focus_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'protection_level': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'rep_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rep_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_conservation_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Designated'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sub_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'tertiary_conservation_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'usmpa_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'verification_reason': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'verification_state': ('django.db.models.fields.CharField', [], {'default': "'Unverified'", 'max_length': '100'}),
            'verified_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'verified_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'wdpa_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wdpa_notes': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'spatialdata.eez': {
            'Meta': {'object_name': 'Eez'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eez': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'eez_id': ('django.db.models.fields.IntegerField', [], {}),
            'gazid': ('django.db.models.fields.FloatField', [], {}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_3digit': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mpas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mpa.Mpa']", 'through': u"orm['spatialdata.EezMembership']", 'symmetrical': 'False'}),
            'nation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['spatialdata.Nation']", 'null': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'geography': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'}),
            'sov_id': ('django.db.models.fields.IntegerField', [], {}),
            'sovereign': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'spatialdata.eezmembership': {
            'Meta': {'object_name': 'EezMembership'},
            'area_in_eez': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eez': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spatialdata.Eez']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mpa.Mpa']"})
        },
        u'spatialdata.meow': {
            'Meta': {'object_name': 'Meow'},
            'alt_code': ('django.db.models.fields.FloatField', [], {}),
            'ecoregion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ecoregion_code': ('django.db.models.fields.FloatField', [], {}),
            'ecoregion_code_x': ('django.db.models.fields.FloatField', [], {}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude_zone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'province_code': ('django.db.models.fields.FloatField', [], {}),
            'realm': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'realm_code': ('django.db.models.fields.FloatField', [], {}),
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'geography': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'})
        },
        u'spatialdata.nation': {
            'Meta': {'object_name': 'Nation'},
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso3code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3'}),
            'marine_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mpa_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mpa_percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'geography': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True'}),
            'summary': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spatialdata']