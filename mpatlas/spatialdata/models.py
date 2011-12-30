from django.contrib.gis.db import models

class Eez(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile  
    eez = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    objectid = models.IntegerField()
    sovereign = models.CharField(max_length=100)
    remarks = models.CharField(max_length=150)
    sov_id = models.IntegerField()
    iso_3digit = models.CharField(max_length=50)
    gazid = models.FloatField()
    eez_id = models.IntegerField()
    area = models.FloatField()
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    #geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    #geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.eez
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc')

class EezSimplified(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile  
    eez = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    objectid = models.IntegerField()
    sovereign = models.CharField(max_length=100)
    remarks = models.CharField(max_length=150)
    sov_id = models.IntegerField()
    iso_3digit = models.CharField(max_length=50)
    gazid = models.FloatField()
    eez_id = models.IntegerField()
    area = models.FloatField()
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    #geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    #geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.eez
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc')

# Auto-generated `LayerMapping` dictionary for Eez model
eez_mapping = {
    'eez' : 'EEZ',
    'country' : 'Country',
    'objectid' : 'ID',
    'sovereign' : 'Sovereign',
    'remarks' : 'Remarks',
    'sov_id' : 'Sov_ID',
    'iso_3digit' : 'ISO_3digit',
    'gazid' : 'GazID',
    'eez_id' : 'eez_ID',
    'area' : 'Area',
    'geom' : 'MULTIPOLYGON',
}

eezsimplified_mapping = {
    'eez' : 'EEZ',
    'country' : 'Country',
    'objectid' : 'ID',
    'sovereign' : 'Sovereign',
    'remarks' : 'Remarks',
    'sov_id' : 'Sov_ID',
    'iso_3digit' : 'ISO_3digit',
    'gazid' : 'GazID',
    'eez_id' : 'EEZ_ID',
    'area' : 'Area',
    'geom' : 'MULTIPOLYGON',
}
