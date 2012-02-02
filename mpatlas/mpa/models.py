from django.contrib.gis.db import models

DESIG_TYPE_CHOICES = (
    ('National', 'National'),
    ('International', 'International'),
    ('ABNJ', 'ABNJ'),
)

IUCN_CAT_CHOICES = (
    ('Ia', 'Ia'),
    ('Ib', 'Ib'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('V', 'V'),
    ('VI', 'VI'),
)

STATUS_CHOICES = (
    ('Proposed', 'Proposed'),
    ('Adopted', 'Adopted'),
    ('Inscribed', 'Inscribed'),
    ('Designated', 'Designated'),
)

NO_TAKE_CHOICES = (
    ('None','None'),
    ('Part','Part'),
    ('All','All'),
    ('Not Reported','Not Reported'),
)

'''
class Mpa(models.Model):
    # Regular fields
    mpa_id = models.IntegerField('MPA id', primary_key=True)
    wdpa_id = models.IntegerField('WDPA id', null=True, blank=True)
    name = models.CharField('Name', max_length=254)
    orig_name = models.CharField('Original Name', max_length=254, null=True, blank=True)
    
    # Set up foreign key to ISO Countries and Sub Locations
    country = models.CharField('Country / Territory', max_length=20)
    sub_loc = models.CharField('Sub Location', max_length=100, null=True, blank=True)
    
    desig = models.CharField('Designation', max_length=254, null=True, blank=True)
    desig_eng = models.CharField('English Designation', max_length=254, null=True, blank=True)
    desig_type = models.CharField('Designation Type', max_length=20, null=True, blank=True, choices=DESIG_TYPE_CHOICES)
    iucn_cat = models.CharField('IUCN Category', max_length=20, null=True, blank=True, choices=IUCN_CAT_CHOICES)
    int_crit = models.CharField('International Criteria', max_length=100, null=True, blank=True)
    marine = models.NullBooleanField('Marine', null=True, blank=True, default=True)
    no_take = models.CharField('No Take', max_length=100, choices=NO_TAKE_CHOICES, default='Not Reported')
    no_take_area = models.FloatField(u'No Take Area km²', null=True, blank=True)
    rep_m_area = models.FloatField(u'Reported Marine Area km²', null=True, blank=True)
    gis_m_area = models.FloatField(u'Calculated Marine Area km²', null=True, blank=True)
    rep_area = models.FloatField(u'Reported Area km²', null=True, blank=True)
    gis_area = models.FloatField(u'Calculated Area km²', null=True, blank=True)
    status = models.CharField('Status', max_length=100, null=True, blank=True, choices=STATUS_CHOICES)
    status_year = models.IntegerField('Status Year', null=True, blank=True)
    gov_type = models.CharField('Governance Type', max_length=254, null=True, blank=True)
    mang_auth = models.CharField('Management Authority', max_length=254, null=True, blank=True)
    mang_plan = models.CharField('Management Plan', max_length=254, null=True, blank=True)
    metadataid = models.IntegerField(null=True, blank=True)
    area_notes = models.CharField('Area Notes', max_length=250, null=True, blank=True)
    
    is_point = models.BooleanField(default=False)
    
    # Full-res polygon features
    geom_smerc = models.MultiPointField(srid=900913, null=True)
    geom = models.MultiPointField(srid=4326, null=True)
    geog = models.MultiPointField(srid=4326, geography=True, null=True)
    
    # Simplified polygon features
    simple_geom_smerc = models.MultiPointField(srid=900913, null=True)
    simple_geom = models.MultiPointField(srid=4326, null=True)
    simple_geog = models.MultiPointField(srid=4326, geography=True, null=True)
    
    # Point location
    point_smerc = models.PointField(srid=900913, null=True)
    point_geom = models.PointField(srid=4326, null=True)
    point_geog = models.PointField(srid=4326, geography=True, null=True)
    
    # Overriding the default manager with a GeoManager instance
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc', 
            'simple_geog', 'simple_geom', 'simple_geom_smerc', 
            'point_geog', 'point_geom', 'point_smerc')

    @property
    def myfields(self):
        d = {}
        for field in MpaCandidate._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d

    @property
    def myfieldslist(self):
        return sorted(self.myfields.items())
'''

class MpaCandidate(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile  
    name = models.CharField(max_length=56)
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPointField(srid=900913, null=True)
    geom = models.MultiPointField(srid=4326, null=True)
    geog = models.MultiPointField(srid=4326, geography=True, null=True)
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
        for field in MpaCandidate._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d

    @property
    def myfieldslist(self):
        return sorted(self.myfields.items())

# Auto-generated `LayerMapping` dictionary for MpaCandidate model
mpacandidate_mapping = {
    'name' : 'NAME',
    'geom' : 'MULTIPOINT',
}
