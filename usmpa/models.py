from django.contrib.gis.db import models

class USMpaPolygon(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile
    site_id = models.CharField(max_length=10)
    site_name = models.CharField(max_length=254)
    site_label = models.CharField(max_length=254)
    gov_level = models.CharField(max_length=254)
    
    state = models.CharField(max_length=254)
    
    ns_full = models.CharField('National System Eligibility', max_length=254)
    protection_level = models.CharField(max_length=254)
    mgmt_plan = models.CharField('Management Plan', max_length=254)
    mgmt_agency = models.CharField('Management Agency', max_length=254)
    fishing_restriction = models.CharField(max_length=254)
    primary_conservation_focus = models.CharField(max_length=254)
    conservation_focus = models.CharField(max_length=254)
    protection_focus = models.CharField(max_length=254)
    permanence = models.CharField(max_length=254)
    constancy = models.CharField(max_length=254)
    establishment_year = models.CharField(max_length=254)
    url = models.CharField(max_length=254)
    url_viewer = models.CharField(max_length=150)
    vessel = models.CharField(max_length=254)
    anchor = models.CharField(max_length=254)
    
    area_km_to = models.FloatField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    area_km_ma = models.FloatField()
    
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPolygonField(srid=900913, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.site_name
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc')
    
    @property
    def myfields(self):
        d = {}
        for field in USMpaPolygon._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d
    
    @property
    def myfieldslist(self):
        return sorted(self.myfields.items())

# Auto-generated `LayerMapping` dictionary for WdpaPolygon model
usmpapolygon_mapping = {
    'site_id' : 'Site_ID',
    'area_km_to' : 'Area_KM_To',
    'shape_leng' : 'Shape_Leng',
    'shape_area' : 'Shape_Area',
    'area_km_ma' : 'Area_KM_Ma',
    'site_name' : 'Site_Name',
    'site_label' : 'Site_Label',
    'gov_level' : 'Gov_Level',
    'ns_full' : 'NS_Full',
    'protection_level' : 'Prot_Lvl',
    'mgmt_plan' : 'Mgmt_Plan',
    'mgmt_agency' : 'Mgmt_Agen',
    'fishing_restriction' : 'Fish_Rstr',
    'primary_conservation_focus' : 'Pri_Con_Fo',
    'protection_focus' : 'Prot_Focus',
    'permanence' : 'Permanence',
    'constancy' : 'Constancy',
    'establishment_year' : 'Estab_Yr',
    'url' : 'URL',
    'vessel' : 'Vessel',
    'anchor' : 'Anchor',
    'conservation_focus' : 'Cons_Focus',
    'url_viewer' : 'URL_Viewer',
    'geog' : 'MULTIPOLYGON',
    #'geom' : 'MULTIPOLYGON',
}
