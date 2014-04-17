# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Campaign'
        db.create_table('campaign_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sub_location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('summary', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('point_geom', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('campaign', ['Campaign'])

        # Adding model 'Initiative'
        db.create_table('campaign_initiative', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal('campaign', ['Initiative'])


    def backwards(self, orm):
        
        # Deleting model 'Campaign'
        db.delete_table('campaign_campaign')

        # Deleting model 'Initiative'
        db.delete_table('campaign_initiative')


    models = {
        'campaign.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'point_geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'sub_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'})
        },
        'campaign.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['campaign']
