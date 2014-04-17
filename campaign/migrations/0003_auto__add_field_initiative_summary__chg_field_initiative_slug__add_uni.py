# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Initiative.summary'
        db.add_column('campaign_initiative', 'summary', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True), keep_default=False)

        # Adding M2M table for field campaigns on 'Initiative'
        db.create_table('campaign_initiative_campaigns', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('initiative', models.ForeignKey(orm['campaign.initiative'], null=False)),
            ('campaign', models.ForeignKey(orm['campaign.campaign'], null=False))
        ))
        db.create_unique('campaign_initiative_campaigns', ['initiative_id', 'campaign_id'])

        # Changing field 'Initiative.slug'
        db.alter_column('campaign_initiative', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=254))

        # Adding index on 'Initiative', fields ['slug']
        db.create_index('campaign_initiative', ['slug'])

        # Adding unique constraint on 'Initiative', fields ['slug']
        db.create_unique('campaign_initiative', ['slug'])

        # Changing field 'Campaign.slug'
        db.alter_column('campaign_campaign', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=254))

        # Adding index on 'Campaign', fields ['slug']
        db.create_index('campaign_campaign', ['slug'])

        # Adding unique constraint on 'Campaign', fields ['slug']
        db.create_unique('campaign_campaign', ['slug'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Campaign', fields ['slug']
        db.delete_unique('campaign_campaign', ['slug'])

        # Removing index on 'Campaign', fields ['slug']
        db.delete_index('campaign_campaign', ['slug'])

        # Removing unique constraint on 'Initiative', fields ['slug']
        db.delete_unique('campaign_initiative', ['slug'])

        # Removing index on 'Initiative', fields ['slug']
        db.delete_index('campaign_initiative', ['slug'])

        # Deleting field 'Initiative.summary'
        db.delete_column('campaign_initiative', 'summary')

        # Removing M2M table for field campaigns on 'Initiative'
        db.delete_table('campaign_initiative_campaigns')

        # Changing field 'Initiative.slug'
        db.alter_column('campaign_initiative', 'slug', self.gf('django.db.models.fields.CharField')(max_length=254))

        # Changing field 'Campaign.slug'
        db.alter_column('campaign_campaign', 'slug', self.gf('django.db.models.fields.CharField')(max_length=254))


    models = {
        'campaign.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'point_geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'sub_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'})
        },
        'campaign.initiative': {
            'Meta': {'object_name': 'Initiative'},
            'campaigns': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['campaign.Campaign']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'summary': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['campaign']
