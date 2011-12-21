from django.contrib.gis.db import models

from django.contrib.gis.measure import Distance

class WdpaPolygon(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile
    objectid = models.IntegerField()
    wdpaid = models.IntegerField()
    wdpa_pid = models.IntegerField()
    name = models.CharField(max_length=254)
    orig_name = models.CharField(max_length=254)
    country = models.CharField(max_length=20)
    sub_loc = models.CharField(max_length=100)
    desig = models.CharField(max_length=254)
    desig_eng = models.CharField(max_length=254)
    desig_type = models.CharField(max_length=20)
    iucn_cat = models.CharField(max_length=20)
    int_crit = models.CharField(max_length=100)
    marine = models.CharField(max_length=20)
    rep_m_area = models.FloatField()
    gis_m_area = models.FloatField()
    rep_area = models.FloatField()
    gis_area = models.FloatField()
    status = models.CharField(max_length=100)
    status_yr = models.IntegerField()
    gov_type = models.CharField(max_length=254)
    mang_auth = models.CharField(max_length=254)
    mang_plan = models.CharField(max_length=254)
    metadataid = models.IntegerField()
    area_notes = models.CharField(max_length=250)
    gis_area_2 = models.FloatField()
    difference = models.FloatField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc')
    
    @property
    def myfields(self):
        d = {}
        for field in WdpaPolygon._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d
    
    @property
    def myfieldslist(self):
        return sorted(self.myfields.items())
    
    @property
    def getnearbyareas(self, limit=5, radius=500):
        toosmall = True
        r = 10
        step = 100
        qs = WdpaPolygon.objects.filter(geog__dwithin=(self.geog, Distance(km=r))).defer(*WdpaPolygon.get_geom_fields())
        while (r <= radius and qs.count() < limit):
            r += step
            qs = WdpaPolygon.objects.filter(geog__dwithin=(self.geog, Distance(km=r))).defer(*WdpaPolygon.get_geom_fields())
        return qs.distance(self.geog, field_name='geog').order_by('distance').defer(*WdpaPolygon.get_geom_fields())[:limit]
        

class WdpaPoint(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile
    objectid = models.IntegerField()
    wdpaid = models.IntegerField()
    wdpa_pid = models.IntegerField()
    name = models.CharField(max_length=254)
    orig_name = models.CharField(max_length=254)
    country = models.CharField(max_length=20)
    sub_loc = models.CharField(max_length=100)
    desig = models.CharField(max_length=254)
    desig_eng = models.CharField(max_length=254)
    desig_type = models.CharField(max_length=20)
    iucn_cat = models.CharField(max_length=20)
    int_crit = models.CharField(max_length=100)
    marine = models.CharField(max_length=20)
    rep_m_area = models.FloatField()
    rep_area = models.FloatField()
    status = models.CharField(max_length=100)
    status_yr = models.IntegerField()
    gov_type = models.CharField(max_length=254)
    mang_auth = models.CharField(max_length=254)
    mang_plan = models.CharField(max_length=254)
    metadataid = models.IntegerField()
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPointField(srid=900913, null=True)
    geom = models.MultiPointField(srid=4326, null=True)
    geog = models.MultiPointField(srid=4326, geography=True, null=True)
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name

# Auto-generated `LayerMapping` dictionary for WdpaPolygon model
wdpapolygon_mapping = {
    'objectid' : 'OBJECTID',
    'wdpaid' : 'WDPAID',
    'wdpa_pid' : 'WDPA_PID',
    'name' : 'NAME',
    'orig_name' : 'ORIG_NAME',
    'country' : 'COUNTRY',
    'sub_loc' : 'SUB_LOC',
    'desig' : 'DESIG',
    'desig_eng' : 'DESIG_ENG',
    'desig_type' : 'DESIG_TYPE',
    'iucn_cat' : 'IUCN_CAT',
    'int_crit' : 'INT_CRIT',
    'marine' : 'MARINE',
    'rep_m_area' : 'REP_M_AREA',
    'gis_m_area' : 'GIS_M_AREA',
    'rep_area' : 'REP_AREA',
    'gis_area' : 'GIS_AREA',
    'status' : 'STATUS',
    'status_yr' : 'STATUS_YR',
    'gov_type' : 'GOV_TYPE',
    'mang_auth' : 'MANG_AUTH',
    'mang_plan' : 'MANG_PLAN',
    'metadataid' : 'METADATAID',
    'area_notes' : 'Area_Notes',
    'gis_area_2' : 'GIS_AREA_2',
    'difference' : 'Difference',
    'shape_leng' : 'Shape_Leng',
    'shape_area' : 'Shape_Area',
    #'geom' : 'MULTIPOLYGON',
    'geog' : 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for WdpaPoint model
wdpapoint_mapping = {
    'objectid' : 'OBJECTID',
    'wdpaid' : 'WDPAID',
    'wdpa_pid' : 'WDPA_PID',
    'name' : 'NAME',
    'orig_name' : 'ORIG_NAME',
    'country' : 'COUNTRY',
    'sub_loc' : 'SUB_LOC',
    'desig' : 'DESIG',
    'desig_eng' : 'DESIG_ENG',
    'desig_type' : 'DESIG_TYPE',
    'iucn_cat' : 'IUCN_CAT',
    'int_crit' : 'INT_CRIT',
    'marine' : 'MARINE',
    'rep_m_area' : 'REP_M_AREA',
    'rep_area' : 'REP_AREA',
    'status' : 'STATUS',
    'status_yr' : 'STATUS_YR',
    'gov_type' : 'GOV_TYPE',
    'mang_auth' : 'MANG_AUTH',
    'mang_plan' : 'MANG_PLAN',
    'metadataid' : 'METADATAID',
    #'geom' : 'MULTIPOINT',
    'geog' : 'MULTIPOINT',
}
