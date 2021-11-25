from django.contrib.gis.db import models

from django.contrib.gis.measure import Distance

class WdpaSource(models.Model):
    metadataid = models.IntegerField()
    data_title = models.CharField(max_length=255)
    resp_party = models.CharField(max_length=255)
    # verifier = models.CharField(max_length=259)
    year = models.CharField(max_length=255)
    update_yr = models.CharField(max_length=255)
    char_set = models.CharField(max_length=255)
    ref_system = models.CharField(max_length=255)
    scale = models.CharField(max_length=255)
    lineage = models.CharField(max_length=264)
    citation = models.CharField(max_length=261)
    disclaimer = models.CharField(max_length=264)
    language = models.CharField(max_length=255)


class WdpaAbstract(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile
    wdpaid = models.FloatField()  # this comes in as float, should we convert to int? No records have 0.X decimal values
    wdpa_pid = models.CharField(max_length=52, blank=True)
    
    pa_def = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=254, blank=True)
    orig_name = models.CharField(max_length=254, blank=True)
    desig = models.CharField(max_length=254, blank=True)
    desig_eng = models.CharField(max_length=254, blank=True)
    desig_type = models.CharField(max_length=20, blank=True)
    iucn_cat = models.CharField(max_length=20, blank=True)
    int_crit = models.CharField(max_length=100, blank=True)
    marine = models.CharField(max_length=20, blank=True)
    no_take = models.CharField(max_length=50, blank=True)
    no_tk_area = models.FloatField(null=True)
    rep_m_area = models.FloatField(null=True)
    rep_area = models.FloatField(null=True)
    status = models.CharField(max_length=100, blank=True)
    status_yr = models.IntegerField(null=True)
    gov_type = models.CharField(max_length=254, blank=True)
    own_type = models.CharField(max_length=254, blank=True)
    mang_auth = models.CharField(max_length=254, blank=True)
    mang_plan = models.CharField(max_length=254, blank=True)
    parent_iso3 = models.CharField(max_length=50, blank=True)
    iso3 = models.CharField(max_length=50)
    sub_loc = models.CharField(max_length=100, blank=True)
    verif = models.CharField(max_length=20, blank=True)
    metadataid = models.IntegerField()
    supp_info = models.CharField(max_length=254, blank=True)
    cons_obj = models.CharField(max_length=100, blank=True)

    gis_area = models.FloatField(null=True)
    gis_m_area = models.FloatField(null=True)
    shape_length = models.FloatField(default=0)
    shape_area = models.FloatField(default=0)

    class Meta:
        abstract = True

    # Returns the string representation of the model.
    def __str__(self):
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


class WdpaPoly_new(WdpaAbstract):
    geom = models.MultiPolygonField(srid=4326, null=True)

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

class WdpaPoint_new(WdpaAbstract):
    geom = models.MultiPointField(srid=4326, null=True)


class WdpaPoly_prev(WdpaAbstract):
    geom = models.MultiPolygonField()

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

class WdpaPoint_prev(WdpaAbstract):
    geom = models.MultiPointField()


# Auto-generated `LayerMapping` dictionary for WDPA_Current model
wdpa2021point_mapping = {
    'wdpaid' : 'WDPAID',
    'wdpa_pid' : 'WDPA_PID',
    'pa_def' : 'PA_DEF',
    'name' : 'NAME',
    'orig_name' : 'ORIG_NAME',
    'desig' : 'DESIG',
    'desig_eng' : 'DESIG_ENG',
    'desig_type' : 'DESIG_TYPE',
    'iucn_cat' : 'IUCN_CAT',
    'int_crit' : 'INT_CRIT',
    'marine' : 'MARINE',
    'rep_m_area' : 'REP_M_AREA',
    'rep_area' : 'REP_AREA',
    'no_take' : 'NO_TAKE',
    'no_tk_area' : 'NO_TK_AREA',
    'status' : 'STATUS',
    'status_yr' : 'STATUS_YR',
    'gov_type' : 'GOV_TYPE',
    'own_type' : 'OWN_TYPE',
    'mang_auth' : 'MANG_AUTH',
    'mang_plan' : 'MANG_PLAN',
    'verif' : 'VERIF',
    'metadataid' : 'METADATAID',
    'sub_loc' : 'SUB_LOC',
    'parent_iso3' : 'PARENT_ISO3',
    'iso3' : 'ISO3',
    'supp_info' : 'SUPP_INFO',
    'cons_obj': 'CONS_OBJ',
    'geom' : 'MULTIPOINT',
}

wdpa2021poly_mapping = wdpa2020point_mapping.copy()
wdpa2021poly_mapping.update({
    'gis_m_area' : 'GIS_M_AREA',
    'gis_area' : 'GIS_AREA',
    'geom' : 'MULTIPOLYGON',
})


# Auto-generated `LayerMapping` dictionary for WDPA_Current model
wdpa2019point_mapping = {
    'wdpaid' : 'WDPAID',
    'wdpa_pid' : 'WDPA_PID',
    'pa_def' : 'PA_DEF',
    'name' : 'NAME',
    'orig_name' : 'ORIG_NAME',
    'desig' : 'DESIG',
    'desig_eng' : 'DESIG_ENG',
    'desig_type' : 'DESIG_TYPE',
    'iucn_cat' : 'IUCN_CAT',
    'int_crit' : 'INT_CRIT',
    'marine' : 'MARINE',
    'rep_m_area' : 'REP_M_AREA',
    'rep_area' : 'REP_AREA',
    'no_take' : 'NO_TAKE',
    'no_tk_area' : 'NO_TK_AREA',
    'status' : 'STATUS',
    'status_yr' : 'STATUS_YR',
    'gov_type' : 'GOV_TYPE',
    'own_type' : 'OWN_TYPE',
    'mang_auth' : 'MANG_AUTH',
    'mang_plan' : 'MANG_PLAN',
    'verif' : 'VERIF',
    'metadataid' : 'METADATAID',
    'sub_loc' : 'SUB_LOC',
    'parent_iso3' : 'PARENT_ISO3',
    'iso3' : 'ISO3',
    'geom' : 'MULTIPOINT',
}


wdpa2019poly_mapping = wdpa2019point_mapping.copy()
wdpa2019poly_mapping.update({
    'gis_m_area' : 'GIS_M_AREA',
    'gis_area' : 'GIS_AREA',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
})

# Auto-generated `LayerMapping` dictionary for WDPA_Current model
wdpa2018point_mapping = {
    'wdpaid' : 'WDPAID',
    'wdpa_pid' : 'WDPA_PID',
    'pa_def' : 'PA_DEF',
    'name' : 'NAME',
    'orig_name' : 'ORIG_NAME',
    'desig' : 'DESIG',
    'desig_eng' : 'DESIG_ENG',
    'desig_type' : 'DESIG_TYPE',
    'iucn_cat' : 'IUCN_CAT',
    'int_crit' : 'INT_CRIT',
    'marine' : 'MARINE',
    'rep_m_area' : 'REP_M_AREA',
    'rep_area' : 'REP_AREA',
    'no_take' : 'NO_TAKE',
    'no_tk_area' : 'NO_TK_AREA',
    'status' : 'STATUS',
    'status_yr' : 'STATUS_YR',
    'gov_type' : 'GOV_TYPE',
    'own_type' : 'OWN_TYPE',
    'mang_auth' : 'MANG_AUTH',
    'mang_plan' : 'MANG_PLAN',
    'verif' : 'VERIF',
    'metadataid' : 'METADATAID',
    'sub_loc' : 'SUB_LOC',
    'parent_iso3' : 'PARENT_ISO3',
    'iso3' : 'ISO3',
    'geom' : 'MULTIPOINT',
}


wdpa2018poly_mapping = wdpa2018point_mapping.copy()
wdpa2018poly_mapping.update({
    'gis_m_area' : 'GIS_M_AREA',
    'gis_area' : 'GIS_AREA',
    'shape_length' : 'Shape_Length',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
})

wdpasource_mapping = {
    'metadataid' : 'metadataid',
    'data_title' : 'data_title',
    'resp_party' : 'resp_party',
    'year' : 'year',
    'update_yr' : 'update_yr',
    'char_set' : 'char_set',
    'ref_system' : 'ref_system',
    'scale' : 'scale',
    'lineage' : 'lineage',
    'citation' : 'citation',
    'disclaimer' : 'disclaimer',
    'language' : 'language',
}

wdpasource_mapping_2019 = {
    'metadataid' : 'METADATAID',
    'data_title' : 'DATA_TITLE',
    'resp_party' : 'RESP_PARTY',
    'verifier' : 'VERIFIER',
    'year' : 'YEAR',
    'update_yr' : 'UPDATE_YR',
    'language' : 'LANGUAGE',
    'char_set' : 'CHAR_SET',
    'ref_system' : 'REF_SYSTEM',
    'scale' : 'SCALE',
    'lineage' : 'LINEAGE',
    'citation' : 'CITATION',
    'disclaimer' : 'DISCLAIMER',
}

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
