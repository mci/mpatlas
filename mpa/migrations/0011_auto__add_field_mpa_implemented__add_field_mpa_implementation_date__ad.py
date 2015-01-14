# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Mpa.implemented'
        db.add_column(u'mpa_mpa', 'implemented',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Mpa.implementation_date'
        db.add_column(u'mpa_mpa', 'implementation_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Mpa.access_info'
        db.add_column(u'mpa_mpa', 'access_info',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Mpa.implemented'
        db.delete_column(u'mpa_mpa', 'implemented')

        # Deleting field 'Mpa.implementation_date'
        db.delete_column(u'mpa_mpa', 'implementation_date')

        # Deleting field 'Mpa.access_info'
        db.delete_column(u'mpa_mpa', 'access_info')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mpa.candidateinfo': {
            'Meta': {'object_name': 'CandidateInfo'},
            'basin': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'current_protection': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desired_protection': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'eez_or_highseas': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'importance': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'key_agency_or_leader': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'lead_organization': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'mpa': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mpa.Mpa']", 'unique': 'True', 'primary_key': 'True'}),
            'opportunity': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'partner_organizations': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'references': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'scope': ('django.db.models.fields.CharField', [], {'default': "'Site'", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'summary': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'timeframe': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
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
            'access_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'implementation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'implemented': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'sovereign': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
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
        u'mpa.mpacandidate': {
            'Meta': {'object_name': 'MpaCandidate'},
            'geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True', 'geography': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'srid': '3857', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '56'})
        },
        u'mpa.versionmetadata': {
            'Meta': {'object_name': 'VersionMetadata'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'revision': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['reversion.Revision']", 'unique': 'True'})
        },
        u'mpa.wikiarticle': {
            'Meta': {'object_name': 'WikiArticle'},
            'mpa': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mpa.Mpa']", 'unique': 'True', 'primary_key': 'True'}),
            'summary': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'reversion.revision': {
            'Meta': {'object_name': 'Revision'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_slug': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '200', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mpa']