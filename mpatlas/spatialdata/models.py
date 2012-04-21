from django.contrib.gis.db import models
from django.db import connection, transaction

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
    geom_smerc = models.MultiPolygonField(srid=3857, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    simple_geom_smerc = models.MultiPolygonField(srid=3857, null=True)
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


class Meow(models.Model):
    ecoregion_code = models.FloatField()
    ecoregion = models.CharField(max_length=50)
    province_code = models.FloatField()
    province = models.CharField(max_length=40)
    realm_code = models.FloatField()
    realm = models.CharField(max_length=40)
    alt_code = models.FloatField()
    ecoregion_code_x = models.FloatField()
    latitude_zone = models.CharField(max_length=10)
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPolygonField(srid=3857, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    simple_geom_smerc = models.MultiPolygonField(srid=3857, null=True)
    simple_geom = models.MultiPolygonField(srid=4326, null=True)
    simple_geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.realm + '_' + self.province + '_' + self.ecoregion
    
    @property
    def name(self):
        return self.realm + '_' + self.province + '_' + self.ecoregion
    
    @property
    def area_km2(self):
        return self.area / 1000.0
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc', 'simple_geog', 'simple_geom', 'simple_geom_smerc')
    
    @classmethod
    def clip_all_geom_at_dateline(cls):
        '''A class method to normalize all geometries crossing to dateline to split cleanly at -180/180 longitude.
            Affects whole table'''
        cursor = connection.cursor()
        cursor.execute("UPDATE spatialdata_meow SET geom = ST_WrapX(ST_WrapX(geom, 0, 360), 180, -360)")
        transaction.commit_unless_managed()
    
    @classmethod
    def set_all_geom_from_geog(cls):
        '''A class method to update all geometry and geography rows from geometry, affects whole table'''
        cursor = connection.cursor()
        cursor.execute("UPDATE spatialdata_meow SET geog = geom::geography, geom_smerc = ST_TRANSFORM(geom, 3857)")
        transaction.commit_unless_managed()
    
    @classmethod
    def set_all_geom_from_geog(cls):
        '''A class method to update all geometry rows from geography, affects whole table'''
        cursor = connection.cursor()
        cursor.execute("UPDATE spatialdata_meow SET geom = geog::geometry, geom_smerc = ST_TRANSFORM(geog::geometry, 3857)")
        transaction.commit_unless_managed()
    
    @classmethod
    def set_all_simple_geom(cls):
        '''A class method to create simplified geometries using tolerance in , affects whole table'''
        cursor = connection.cursor()
        cursor.execute("UPDATE spatialdata_meow SET simple_geom_smerc = ST_Multi(ST_SimplifyPreserveTopology(geom_smerc, 500))")
        cursor.execute("UPDATE spatialdata_meow SET simple_geom = ST_TRANSFORM(simple_geom_smerc, 4326), simple_geog = ST_TRANSFORM(simple_geom_smerc, 4326)::geography")
        transaction.commit_unless_managed()

# Auto-generated `LayerMapping` dictionary for Meow model
meow_mapping = {
    'ecoregion_code' : 'ECO_CODE',
    'ecoregion' : 'ECOREGION',
    'province_code' : 'PROV_CODE',
    'province' : 'PROVINCE',
    'realm_code' : 'RLM_CODE',
    'realm' : 'REALM',
    'alt_code' : 'ALT_CODE',
    'ecoregion_code_x' : 'ECO_CODE_X',
    'latitude_zone' : 'Lat_Zone',
    'geom' : 'MULTIPOLYGON',
}

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
