# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Mpa'
        db.create_table('mpa_mpa', (
            ('mpa_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wdpa_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('usmpa_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sub_location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('designation_eng', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('designation_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('iucn_category', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('int_criteria', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('marine', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Designated', max_length=100, null=True, blank=True)),
            ('status_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('no_take', self.gf('django.db.models.fields.CharField')(default='Not Reported', max_length=100)),
            ('no_take_area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rep_m_area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('calc_m_area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rep_area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('calc_area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gov_type', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('mgmt_auth', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('mgmt_plan_type', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('mgmt_plan_ref', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='mpa_main_set', null=True, to=orm['mpa.Contact'])),
            ('conservation_effectiveness', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('protection_level', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('fishing', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('fishing_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fishing_citation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('access_citation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('primary_conservation_focus', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('secondary_conservation_focus', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('tertiary_conservation_focus', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('conservation_focus_citation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('protection_focus', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('protection_focus_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('protection_focus_citation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('constancy', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('constancy_citation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('permanence', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=254, null=True, blank=True)),
            ('permanence_citation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('wdpa_notes', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_point', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=3857, null=True, blank=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('simple_geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=3857, null=True, blank=True)),
            ('simple_geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('simple_geog', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
            ('point_geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(srid=3857, null=True, blank=True)),
            ('point_geom', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True, blank=True)),
            ('point_geog', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True, blank=True)),
            ('point_within', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('bbox_lowerleft', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('bbox_upperright', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('mpa', ['Mpa'])

        # Adding M2M table for field other_contacts on 'Mpa'
        db.create_table('mpa_mpa_other_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mpa', models.ForeignKey(orm['mpa.mpa'], null=False)),
            ('contact', models.ForeignKey(orm['mpa.contact'], null=False))
        ))
        db.create_unique('mpa_mpa_other_contacts', ['mpa_id', 'contact_id'])

        # Adding model 'WikiArticle'
        db.create_table('mpa_wikiarticle', (
            ('mpa', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mpa.Mpa'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mpa', ['WikiArticle'])

        # Adding model 'Contact'
        db.create_table('mpa_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('address', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mpa', ['Contact'])

        # Adding model 'VersionMetadata'
        db.create_table('mpa_versionmetadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['reversion.Revision'], unique=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('reference', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mpa', ['VersionMetadata'])

        # Adding model 'MpaCandidate'
        db.create_table('mpa_mpacandidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('geom_smerc', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(srid=900913, null=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True)),
            ('geog', self.gf('django.contrib.gis.db.models.fields.MultiPointField')(null=True)),
        ))
        db.send_create_signal('mpa', ['MpaCandidate'])


    def backwards(self, orm):
        
        # Deleting model 'Mpa'
        db.delete_table('mpa_mpa')

        # Removing M2M table for field other_contacts on 'Mpa'
        db.delete_table('mpa_mpa_other_contacts')

        # Deleting model 'WikiArticle'
        db.delete_table('mpa_wikiarticle')

        # Deleting model 'Contact'
        db.delete_table('mpa_contact')

        # Deleting model 'VersionMetadata'
        db.delete_table('mpa_versionmetadata')

        # Deleting model 'MpaCandidate'
        db.delete_table('mpa_mpacandidate')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 11, 9, 12, 35, 298391)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 11, 9, 12, 35, 298294)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'bbox_lowerleft': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'bbox_upperright': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'calc_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'calc_m_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'conservation_effectiveness': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'conservation_focus_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'constancy': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'constancy_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mpa_main_set'", 'null': 'True', 'to': "orm['mpa.Contact']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'designation_eng': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'designation_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fishing': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'fishing_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fishing_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
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
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mpa.Contact']", 'null': 'True', 'blank': 'True'}),
            'permanence': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'permanence_citation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'point_geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True', 'blank': 'True'}),
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
            'simple_geog': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'simple_geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'simple_geom_smerc': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Designated'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sub_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tertiary_conservation_focus': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'usmpa_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'wdpa_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wdpa_notes': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'mpa.mpacandidate': {
            'Meta': {'object_name': 'MpaCandidate'},
            'geog': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'null': 'True'}),
            'geom_smerc': ('django.contrib.gis.db.models.fields.MultiPointField', [], {'srid': '900913', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '56'})
        },
        'mpa.versionmetadata': {
            'Meta': {'object_name': 'VersionMetadata'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'revision': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['reversion.Revision']", 'unique': 'True'})
        },
        'mpa.wikiarticle': {
            'Meta': {'object_name': 'WikiArticle'},
            'mpa': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mpa.Mpa']", 'unique': 'True', 'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'reversion.revision': {
            'Meta': {'object_name': 'Revision'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_slug': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '200', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mpa']
