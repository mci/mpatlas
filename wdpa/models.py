from django.contrib.gis.db import models

from django.contrib.gis.measure import Distance

class WdpaAbstract(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile
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
    rep_m_area = models.FloatField(null=True)
    rep_area = models.FloatField(null=True)
    status = models.CharField(max_length=100)
    status_yr = models.IntegerField(null=True)
    gov_type = models.CharField(max_length=254)
    mang_auth = models.CharField(max_length=254)
    mang_plan = models.CharField(max_length=254)
    metadataid = models.IntegerField()

    class Meta:
        abstract = True

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc')

    @property
    def get_point_within(self):
        '''Get a point on the geometry surface.
            Use a point already in the db if possible, otherwise calculate and save one.
        '''
        if self.point_within is None:
            # Make PostGIS calculate this for us
            me = self.__class__.objects.centroid(field_name='geom').point_on_surface(field_name='geom').only('geom').get(pk=self.pk)
            # if the centroid intersects the polygon, use it, otherwise return the point_on_surface
            centroid_inside = self.__class__.objects.filter(pk=self.pk, geom__intersects=me.centroid).count()
            self.point_within = me.centroid if centroid_inside else me.point_on_surface
            self.point_within_geojson = self.point_within.geojson
            self.save()
        return self.point_within_geojson
    
    @property
    def get_bbox(self):
        '''Get the geometry bounding box.
            Use a shape already in the db if possible, otherwise calculate and save one.
        '''
        if self.bbox is None:
            # Make PostGIS calculate this for us
            me = self.__class__.objects.envelope(field_name='geom').only('id').get(pk=self.pk)
            self.bbox = me.envelope
            self.bbox_geojson = self.bbox.geojson
            self.save()
        return self.bbox_geojson

    @property
    def myfields(self):
        d = {}
        for field in WdpaPolygon._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d
    
    @property
    def myfieldslist(self):
        return sorted(self.myfields.items())

class Wdpa2014Polygon(WdpaAbstract):
    updateme = models.BooleanField(default=False)
    new = models.BooleanField(default=False)

    no_take = models.CharField(max_length=50)
    no_tk_area = models.FloatField()
    parent_iso3 = models.CharField(max_length=100)

    gis_area = models.FloatField(null=True)
    gis_m_area = models.FloatField(null=True)
    shape_leng = models.FloatField(default=0)
    shape_area = models.FloatField(default=0)

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)

    # Calculated geometry fields
    point_within = models.PointField(srid=4326, null=True)
    point_within_geojson = models.TextField(null=True)
    bbox = models.PolygonField(srid=4326, null=True)
    bbox_geojson = models.TextField(null=True)
    
    @property
    def get_nearby_areas(self, limit=5, radius=500):
        toosmall = True
        r = 10
        step = 100
        qs = WdpaPolygon.objects.filter(geog__dwithin=(self.geog, Distance(km=r))).defer(*WdpaPolygon.get_geom_fields())
        while (r <= radius and qs.count() < limit):
            r += step
            qs = WdpaPolygon.objects.filter(geog__dwithin=(self.geog, Distance(km=r))).defer(*WdpaPolygon.get_geom_fields())
        return qs.distance(self.geog, field_name='geog').order_by('distance').defer(*WdpaPolygon.get_geom_fields())[:limit]
        

class Wdpa2014Point(WdpaAbstract):
    updateme = models.BooleanField(default=False)
    new = models.BooleanField(default=False)

    no_take = models.CharField(max_length=50)
    no_tk_area = models.FloatField()
    parent_iso3 = models.CharField(max_length=100)

    gis_area = models.FloatField(null=True)
    gis_m_area = models.FloatField(null=True)
    shape_leng = models.FloatField(default=0)
    shape_area = models.FloatField(default=0)

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPointField(srid=900913, null=True)
    geom = models.MultiPointField(srid=4326, null=True)
    geog = models.MultiPointField(srid=4326, geography=True, null=True)


class WdpaPolygon(WdpaAbstract):
    objectid = models.IntegerField()

    gis_area = models.FloatField(null=True)
    gis_area_2 = models.FloatField(default=0)
    gis_m_area = models.FloatField(null=True)
    difference = models.FloatField(default=0)
    area_notes = models.CharField(max_length=250)
    shape_leng = models.FloatField(default=0)
    shape_area = models.FloatField(default=0)

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)

    # Calculated geometry fields
    point_within = models.PointField(srid=4326, null=True)
    point_within_geojson = models.TextField(null=True)
    bbox = models.PolygonField(srid=4326, null=True)
    bbox_geojson = models.TextField(null=True)

    
    @property
    def get_nearby_areas(self, limit=5, radius=500):
        toosmall = True
        r = 10
        step = 100
        qs = WdpaPolygon.objects.filter(geog__dwithin=(self.geog, Distance(km=r))).defer(*WdpaPolygon.get_geom_fields())
        while (r <= radius and qs.count() < limit):
            r += step
            qs = WdpaPolygon.objects.filter(geog__dwithin=(self.geog, Distance(km=r))).defer(*WdpaPolygon.get_geom_fields())
        return qs.distance(self.geog, field_name='geog').order_by('distance').defer(*WdpaPolygon.get_geom_fields())[:limit]
        

class WdpaPoint(WdpaAbstract):
    objectid = models.IntegerField()

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPointField(srid=900913, null=True)
    geom = models.MultiPointField(srid=4326, null=True)
    geog = models.MultiPointField(srid=4326, geography=True, null=True)


# Auto-generated `LayerMapping` dictionary for WdpaPolygon model
wdpa2014polygon_mapping = {
    'wdpaid' : 'WDPAID',
    'wdpa_pid' : 'WDPA_PID',
    'name' : 'NAME',
    'orig_name' : 'ORIG_NAME',
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
    'no_take' : 'NO_TAKE',
    'no_tk_area' : 'NO_TK_AREA',
    'metadataid' : 'METADATAID',
    'parent_iso3' : 'PARENT_ISO3',
    'country' : 'ISO3',
    'shape_leng' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

wdpa2014point_mapping = {
    'wdpaid' : 'WDPAID',
    'wdpa_pid' : 'WDPA_PID',
    'name' : 'NAME',
    'orig_name' : 'ORIG_NAME',
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
    'no_take' : 'NO_TAKE',
    'no_tk_area' : 'NO_TK_AREA',
    'metadataid' : 'METADATAID',
    'country' : 'ISO3',
    'parent_iso3' : 'PARENT_ISO3',
    'geom' : 'MULTIPOINT',
}



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
