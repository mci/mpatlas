# -*- coding: utf-8 -*-
# Do not remove, we're using some special characters
# in string literals below

from django.contrib.gis.db import models
from django.contrib.gis import geos, gdal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection, transaction

DESIG_TYPE_CHOICES = (
    ('National', 'National'),
    ('International', 'International'),
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
    ('Restricted', 'Restricted'),
)

CONSERVATION_FOCUS_CHOICES = (
    ('Unknown', 'Unknown'),
    ('Biodiversity Protection', 'Biodiversity Protection'),
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
    ('Non-Permanent - Conditional', 'Non-Permanent - Conditional'),
    ('Non-Permanent - Temporary', 'Non-Permanent - Temporary'),
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
    usmpa_id = models.CharField('US MPA id', max_length=50, null=True, blank=True)
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
    mgmt_plan_type = models.CharField('Management Plan Type', max_length=254, null=True, blank=True)
    mgmt_plan_ref = models.CharField('Management Plan Reference', max_length=254, null=True, blank=True)
    
    # Contact
    contact = models.ForeignKey('Contact', related_name='mpa_main_set', verbose_name='Main Contact', null=True)
    other_contacts = models.ManyToManyField('Contact', verbose_name='Other Contacts', null=True)
    
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
    geom_smerc = models.MultiPolygonField(srid=3857, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    # Simplified polygon features
    simple_geom_smerc = models.MultiPolygonField(srid=3857, null=True)
    simple_geom = models.MultiPolygonField(srid=4326, null=True)
    simple_geog = models.MultiPolygonField(srid=4326, geography=True, null=True)
    
    # Point location, used when we don't have polygon boundaries
    point_geom_smerc = models.MultiPointField(srid=3857, null=True)
    point_geom = models.MultiPointField(srid=4326, null=True)
    point_geog = models.MultiPointField(srid=4326, geography=True, null=True)
    
    # Point somewhere within the site
    point_within = models.PointField(srid=4326, null=True)
    
    # bounding box of polygon
    # assume longitude range is < 180 degrees, bbox can cross dateline
    bbox_lowerleft = models.PointField(srid=4326, null=True)
    bbox_upperright = models.PointField(srid=4326, null=True)
    
    # Overriding the default manager with a GeoManager instance
    objects = models.GeoManager()
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc', 
            'simple_geog', 'simple_geom', 'simple_geom_smerc', 
            'point_geog', 'point_geom', 'point_geom_smerc')

    @property
    def myfields(self):
        d = {}
        for field in MpaCandidate._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d

    @property
    def myfieldslist(self):
        return sorted(self.myfields.items())
    
    # Keep ourselves from having to always test if onetoone exists for wikiarticle
    @property
    def get_wikiarticle(self):
        try:
            return self.wikiarticle
        except:
            return None
    
    def set_point_within(self):
        '''Get a point on the geometry surface.
            Use a point already in the db if possible, otherwise calculate and save one.
        '''
        # Make PostGIS calculate this for us
        try:
            if self.is_point:
                self.point_within = self.point_geom
            else:
                me = self.__class__.objects.centroid(field_name='geom').point_on_surface(field_name='geom').only('geom').get(pk=self.pk)
                # if the centroid intersects the polygon, use it, otherwise return the point_on_surface
                centroid_inside = self.__class__.objects.filter(pk=self.pk, geom__intersects=me.centroid).count()
                self.point_within = me.centroid if centroid_inside else me.point_on_surface
            self.save()
            return self.point_within
        except:
            return None

    def set_bbox(self):
        '''Get the geometry bounding box.
            Use a shape already in the db if possible, otherwise calculate and save one.
        '''
        # This will return a full-width box (-180 to 180) for multipolygons that cross the dateline -- NEED TO FIX
        # Make PostGIS calculate this for us
        try:
            if self.is_point:
                self.bbox_lowerleft = self.point_geom
                self.bbox_upperright = self.point_geom
            else:
                me = self.__class__.objects.extent(field_name='geom').only('id').get(pk=self.pk)
                me.extent
                self.bbox_lowerleft = geos.Point(me.extent[0], me.extent[1], srid=gdal.SpatialReference('WGS84').srid)
                self.bbox_upperright = geos.Point(me.extent[2], me.extent[3], srid=gdal.SpatialReference('WGS84').srid)
            self.save()
            return (self.bbox_lowerleft, self.bbox_upperright)
        except:
            return None
    
    def set_geom_from_geog(self):
        # Raw SQL update geometry fields, much faster than through django
        cursor = connection.cursor()
        cursor.execute("UPDATE mpa_mpa SET geom = geog::geometry, geom_smerc = ST_TRANSFORM(geog::geometry, 3857) WHERE mpa_id = %s" , [self.mpa_id])
        cursor.execute("UPDATE mpa_mpa SET point_geom = point_geog::geometry, point_geom_smerc = ST_TRANSFORM(point_geog::geometry, 3857) WHERE mpa_id = %s" , [self.mpa_id])
        transaction.commit_unless_managed()
    
    @classmethod
    def set_all_geom_from_geog(cls):
        '''A class method to update all geometry rows from geography, affects whole table'''
        cursor = connection.cursor()
        cursor.execute("UPDATE mpa_mpa SET geom = geog::geometry, geom_smerc = ST_TRANSFORM(geog::geometry, 3857)")
        cursor.execute("UPDATE mpa_mpa SET point_geom = point_geog::geometry, point_geom_smerc = ST_TRANSFORM(point_geog::geometry, 3857)")
        transaction.commit_unless_managed()

@receiver(post_save, sender=Mpa)
def mpa_post_save(sender, instance, *args, **kwargs):
    # Calculate things once an mpa object is created or updated
    # Disconnect post_save so we don't enter recursive loop
    post_save.disconnect(mpa_post_save, sender=Mpa)
    instance.set_point_within()
    instance.set_bbox()
    post_save.connect(mpa_post_save, sender=Mpa)


class WikiArticle(models.Model):
    mpa = models.OneToOneField(Mpa, primary_key=True)
    url = models.URLField('Link to Wikipedia Article', null=True, blank=True)
    summary = models.TextField('MPA Site Description from Wikipedia', null=True, blank=True)


class Contact(models.Model):
    agency = models.CharField(max_length=500)
    url = models.URLField(max_length=500)
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
