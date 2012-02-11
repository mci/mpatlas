# -*- coding: utf-8 -*-
# Do not remove, we're using some special characters
# in string literals below

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

PROTECTION_LEVEL_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Strongly Protected','Strongly Protected'),
    ('Moderately Protected','Moderately Protected'),
    ('Protected','Protected'),
    ('Managed','Managed'),
)

FISHING_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Some Restrictions', 'Some Restrictions'),
)

ACCESS_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Yes', 'Yes'),
    ('No', 'No'),
)

CONSERVATION_FOCUS_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Biodiversity Protection'),
    ('Biomass Enhancement', 'Biomass Enhancement'),
    ('Cultural Heritage', 'Cultural Heritage'),
)

PROTECTION_FOCUS_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Ecosystem', 'Ecosystem'),
    ('Focal Species', 'Focal Species'),
)

CONSTANCY_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Year-round', 'Year-round'),
    ('Seasonal', 'Seasonal'),
    ('Temporary', 'Temporary'),
)

PERMANENCE_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Permanent', 'Permanent'),
    ('Non-Permanent', 'Non-Permanent'),
)

CONSERVATION_EFFECTIVENESS_CHOICES = (
    ('Unknown', 'Unknown'),
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
)


class Mpa(models.Model):
    # ID / Name
    mpa_id = models.AutoField('MPA id', primary_key=True)
    wdpa_id = models.IntegerField('WDPA id', null=True, blank=True)
    usmpa_id = models.IntegerField('US MPA id', null=True, blank=True)
    name = models.CharField('Name', max_length=254)
    long_name = models.CharField(max_length=254) # name + designation
    short_name = models.CharField(max_length=254) # name + designation with abbreviations
    slug = models.CharField(max_length=254)
    
    # Set up foreign key to ISO Countries and Sub Locations
    country = models.CharField('Country / Territory', max_length=20)
    sub_location = models.CharField('Sub Location', max_length=100, null=True, blank=True)
    
    # Designation
    designation = models.CharField('Designation', max_length=254, null=True, blank=True)
    designation_eng = models.CharField('English Designation', max_length=254, null=True, blank=True)
    designation_type = models.CharField('Designation Type', max_length=20, null=True, blank=True, choices=DESIG_TYPE_CHOICES)
    iucn_category = models.CharField('IUCN Category', max_length=20, null=True, blank=True, choices=IUCN_CAT_CHOICES)
    int_criteria = models.CharField('International Criteria', max_length=100, null=True, blank=True)
    marine = models.NullBooleanField('Marine', null=True, blank=True, default=True)
    status = models.CharField('Status', max_length=100, null=True, blank=True, choices=STATUS_CHOICES, default='Designated')
    status_year = models.IntegerField('Status Year', null=True, blank=True)
    
    # Area Estimates
    no_take = models.CharField('No Take', max_length=100, choices=NO_TAKE_CHOICES, default='Not Reported')
    no_take_area = models.FloatField(u'No Take Area km²', null=True, blank=True)
    rep_m_area = models.FloatField(u'Reported Marine Area km²', null=True, blank=True)
    calc_m_area = models.FloatField(u'Calculated Marine Area km²', null=True, blank=True)
    rep_area = models.FloatField(u'Reported Area km²', null=True, blank=True)
    calc_area = models.FloatField(u'Calculated Area km²', null=True, blank=True)
    
    # Management details
    gov_type = models.CharField('Governance Type', max_length=254, null=True, blank=True) # = US gov_level
    mgmt_auth = models.CharField('Management Authority', max_length=254, null=True, blank=True)
    mgmt_plan_type = models.CharField('Management Plan Type', max_length=254)
    mgmt_plan_ref = models.CharField('Management Plan Reference', max_length=254, null=True, blank=True)
    
    # Contact
    contact = models.ForeignKeyField(Contact, verbose_name='Main Contact')
    other_contacts = models.ManyToManyField(Contact, verbose_name='Other Contacts')
    
    #Conservation Effectiveness
    conservation_effectiveness = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_EFFECTIVENESS_CHOICES, default='Unknown')
    
    # Protection Level
    protection_level = models.CharField(max_length=254, null=True, blank=True, choices=PROTECTION_LEVEL_CHOICES, default='Unknown')
    fishing = models.CharField(max_length=254, null=True, blank=True, choices=FISHING_CHOICES, default='Unknown')
    fishing_info = models.TextField(null=True, blank=True)
    fishing_citation = models.TextField(null=True, blank=True)
    access = models.CharField(max_length=254, null=True, blank=True, choices=ACCESS_CHOICES, default='Unknown')
    access_citation = models.TextField(null=True, blank=True)
    
    # Conservation Focus
    primary_conservation_focus = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_FOCUS_CHOICES, default='Unknown')
    secondary_conservation_focus = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_FOCUS_CHOICES, default='Unknown')
    tertiary_conservation_focus = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_FOCUS_CHOICES, default='Unknown')
    conservation_focus_citation = models.TextField(null=True, blank=True)
    
    # Protection Focus
    protection_focus = models.CharField(max_length=254, null=True, blank=True, choices=PROTECTION_FOCUS_CHOICES, default='Unknown')
    protection_focus_info = models.TextField(null=True, blank=True)
    protection_focus_citation = models.TextField(null=True, blank=True)
    
    constancy = models.CharField(max_length=254, null=True, blank=True, choices=CONSTANCY_CHOICES, default='Unknown')
    constancy_citation = models.TextField(null=True, blank=True)
    permanence = models.CharField(max_length=254, null=True, blank=True, choices=PERMANENCE_CHOICES, default='Unknown')
    permanence_citation = models.TextField(null=True, blank=True)
    
    # Notes
    wdpa_notes = models.CharField('Area Notes (from WDPA)', max_length=250, null=True, blank=True)
    notes = models.TextField('Area Notes')
    
    # Summary Info
    summary = models.TextField('MPA Summary Site Description', null=True, blank=True)
    
    ## GEOGRAPHY
    is_point = models.BooleanField(default=False)
    
    # Full-res polygon features
    # If is_point is true, this will be a box or circle based on the 
    # area estimate (calculated from local UTM crs or a global equal area crs)
    geom_smerc = models.MultiPointField(srid=900913, null=True)
    geom = models.MultiPointField(srid=4326, null=True)
    geog = models.MultiPointField(srid=4326, geography=True, null=True)
    
    # Simplified polygon features
    simple_geom_smerc = models.MultiPointField(srid=900913, null=True)
    simple_geom = models.MultiPointField(srid=4326, null=True)
    simple_geog = models.MultiPointField(srid=4326, geography=True, null=True)
    
    # Point location
    point_smerc = models.MultiPointField(srid=900913, null=True)
    point_geom = models.MultiPointField(srid=4326, null=True)
    point_geog = models.MultiPointField(srid=4326, geography=True, null=True)
    
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


class WikiArticle(models.Model):
    mpa = models.OneToOneField(Mpa, primary_key=True)
    url = models.UrlField('Link to Wikipedia Article', null=True, blank=True)
    summary = models.TextField('MPA Site Description from Wikipedia', null=True, blank=True)


class Contact(models.Model):
    agency = models.CharField(max_length=500)
    url = models.UrlField(max_length=500)
    address = models.TextField()

# class MpaCandidateInfo(models.Model):
#     pass


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
