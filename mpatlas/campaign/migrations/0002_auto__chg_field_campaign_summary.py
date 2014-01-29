# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Campaign.summary'
        db.alter_column('campaign_campaign', 'summary', self.gf('ckeditor.fields.RichTextField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'Campaign.summary'
        db.alter_column('campaign_campaign', 'summary', self.gf('tinymce.models.HTMLField')(null=True))


    models = {
        'campaign.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'point_geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'sub_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'})
        },
        'campaign.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['campaign']
