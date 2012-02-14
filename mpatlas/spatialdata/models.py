from django.contrib.gis.db import models

class Nation(models.Model):
    name = models.CharField(max_length=240)
    #iso3code = models.ForeignKey(country_iso)
    summary = models.TextField()

class Eez(models.Model):
    # Regular fields corresponding to attributes in shpfile  
    eez = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    objectid = models.IntegerField()
    sovereign = models.CharField(max_length=100)
    nation = models.ForeignKey(Nation, null=True, default=None)
    remarks = models.CharField(max_length=150)
    sov_id = models.IntegerField()
    iso_3digit = models.CharField(max_length=50)
    gazid = models.FloatField()
    eez_id = models.IntegerField()
    area = models.FloatField()
    
    # Spatial analyses and stats for MPAs
    mpas = models.ManyToManyField('mpa.Mpa', through='EezMembership', verbose_name="MPAs within this EEZ")
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    simple_geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    simple_geom = models.MultiPolygonField(srid=4326, null=True)
    simple_geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.eez
    
    @property
    def name(self):
        return self.eez
    
    @property
    def area_km2(self):
        return self.area / 1000.0
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc', 'simple_geog', 'simple_geom', 'simple_geom_smerc')

class EezMembership(models.Model):
    eez = models.ForeignKey(Eez)
    mpa = models.ForeignKey('mpa.Mpa')
    area_in_eez = models.FloatField('mpa area in eez (m2)', null=True)

class EezSimplified(models.Model):
    # Regular fields corresponding to attributes in shpfile  
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
    geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
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
