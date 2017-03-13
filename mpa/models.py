# -*- coding: utf-8 -*-
# Do not remove, we're using some special characters
# in string literals below

from django.contrib.gis.db import models
from django.contrib.gis import geos, gdal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection, transaction
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from BeautifulSoup import BeautifulSoup

# import reversion
from reversion import revisions as reversion
from reversion.models import Revision

from taggit.managers import TaggableManager
from category.models import TaggedItem

from spatialdata.models import Nation

from collections import OrderedDict

# fields variable is overwritten at end of module, listing all fields needed to pull from mpatlas
# via a .values(*fields) call.  Update this for new columns.
mpa_export_fields = []

VERIFY_CHOICES = (
    ('Unverified', 'Unverified'),
    ('Cannot Verify', 'Cannot Verify'),
    ('Rejected as MPA', 'Rejected as MPA'),
    ('Internally Verified', 'Internally Verified'),
    ('Externally Verified', 'Externally Verified'),
)

MPA_TYPE_CHOICES = (
    ('Marine Protected Area', 'Marine Protected Area'),
    ('(Non-MPA) Fisheries Management Zone', '(Non-MPA) Fisheries Management Zone'),
    ('(Non-MPA) Other Marine Managed Area', '(Non-MPA) Other Marine Managed Area'),
    ('(Non-MPA) Terrestrial Area without Marine Component', '(Non-MPA) Terrestrial Area without Marine Component'),
)

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
    # ('Adopted', 'Adopted'),
    # ('Inscribed', 'Inscribed'),
    ('Designated', 'Designated'),
    ('Defunct/Degazetted', 'Defunct/Degazetted'),
)

IMPLEMENTED_CHOICES = (
    ('Not Implemented', 'Not Implemented'),
    ('Implemented', 'Implemented'),
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
    mpa_id = models.AutoField('MPA id', primary_key=True, editable=False)
    wdpa_id = models.IntegerField('WDPA id', null=True, blank=True, help_text='WDPA ID code. You probably should not be changing this.')
    usmpa_id = models.CharField('US MPA id', max_length=50, null=True, blank=True, help_text='US NOAA MPA Center ID. You probably should not be changing this.')
    other_ids = models.CharField('Other reference id codes', max_length=1000, null=True, blank=True, help_text='ID codes used by other groups to identify this area, e.g., TNC Caribbean or Coral Triangle Atlas ids.')
    name = models.CharField('Name', max_length=254, help_text='Protected area name not including designation title')
    long_name = models.CharField(max_length=254, blank=True) # name + designation
    short_name = models.CharField(max_length=254, blank=True, help_text='Nickname if any') # name + designation with abbreviations
    slug = models.CharField(max_length=254, blank=True)

    # Taggit TaggableManger used to define categories
    categories = TaggableManager(through=TaggedItem, verbose_name='Categories', help_text='You can assign this area to one or more categories by providing a comma-separated list of tags enclosed in quotes (e.g., [ "Shark Sanctuary", "World Heritage Site" ]', blank=True)
    
    # Set up foreign key to ISO Countries and Sub Locations
    sovereign = models.CharField('Sovereign Country', max_length=50, null=True, blank=True)
    country = models.CharField('Country / Territory', max_length=50)
    sub_location = models.CharField('Sub Location', max_length=100, null=True, blank=True)
    
    # Verification State
    is_mpa = models.BooleanField(default=True)
    verification_state = models.CharField('Verification State', max_length=100, default='Unverified', choices=VERIFY_CHOICES)
    verification_reason = models.CharField('Verification Reason', max_length=1000, null=True, blank=True)
    verified_by = models.CharField('Verified By', max_length=100, null=True, blank=True)
    verified_date = models.DateField('Date Verified', null=True, blank=True)
    
    # Designation
    designation = models.CharField('Designation', max_length=254, null=True, blank=True)
    designation_eng = models.CharField('English Designation', max_length=254, null=True, blank=True)
    designation_type = models.CharField('Designation Type', max_length=20, null=True, blank=True, choices=DESIG_TYPE_CHOICES)
    iucn_category = models.CharField('IUCN Category', max_length=20, null=True, blank=True, choices=IUCN_CAT_CHOICES)
    int_criteria = models.CharField('International Criteria', max_length=100, null=True, blank=True)
    marine = models.NullBooleanField('Marine (field from WDPA)', null=True, blank=True, default=True, editable=False)
    status = models.CharField('Status', max_length=100, null=True, blank=True, choices=STATUS_CHOICES, default='Designated')
    status_year = models.IntegerField('Status Year', null=True, blank=True)

    # Implementation
    implemented = models.BooleanField('Implemented?', help_text='MPA is designated and implemented with regulations enforced', blank=True, default=True)
    implementation_date = models.DateField('Implementation Date', help_text='Date regulations went into effect or will go into effect', null=True, blank=True)
    
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
    contact = models.ForeignKey('Contact', related_name='mpa_main_set', verbose_name='Main Contact', null=True, blank=True)
    other_contacts = models.ManyToManyField('Contact', verbose_name='Other Contacts', blank=True)
    
    #Conservation Effectiveness
    conservation_effectiveness = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_EFFECTIVENESS_CHOICES, default='Unknown')
    
    # Protection Level
    protection_level = models.CharField(max_length=254, null=True, blank=True, choices=PROTECTION_LEVEL_CHOICES, default='Unknown', editable=False)
    fishing = models.CharField(max_length=254, null=True, blank=True, choices=FISHING_CHOICES, default='Unknown')
    fishing_info = models.TextField(null=True, blank=True)
    fishing_citation = models.TextField(null=True, blank=True)
    access = models.CharField(max_length=254, null=True, blank=True, choices=ACCESS_CHOICES, default='Unknown')
    access_info = models.TextField(null=True, blank=True)
    access_citation = models.TextField(null=True, blank=True)
    
    # Conservation Focus
    primary_conservation_focus = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_FOCUS_CHOICES, default='Unknown')
    secondary_conservation_focus = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_FOCUS_CHOICES, default='Unknown')
    tertiary_conservation_focus = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_FOCUS_CHOICES, default='Unknown')
    conservation_focus_info = models.TextField(null=True, blank=True)
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
    wdpa_notes = models.CharField('Area Notes (from WDPA)', max_length=250, null=True, blank=True, editable=False)
    notes = models.TextField('Area Notes', null=True, blank=True, default='')
    
    # Summary Info
    summary = RichTextField('MPA Summary Site Description', null=True, blank=True)
    
    ## GEOGRAPHY
    is_point = models.BooleanField(default=False)
    
    # Full-res polygon features
    # If is_point is true, this will be a box or circle based on the 
    # area estimate (calculated from local UTM crs or a global equal area crs)
    geom_smerc = models.MultiPolygonField(srid=3857, null=True, blank=True, editable=False)
    geom = models.MultiPolygonField(srid=4326, null=True, blank=True, editable=False)
    geog = models.MultiPolygonField(srid=4326, geography=True, null=True, blank=True, editable=False)
    
    # Simplified polygon features
    simple_geom_smerc = models.MultiPolygonField(srid=3857, null=True, blank=True, editable=False)
    simple_geom = models.MultiPolygonField(srid=4326, null=True, blank=True, editable=False)
    simple_geog = models.MultiPolygonField(srid=4326, geography=True, null=True, blank=True, editable=False)
    
    # Point location, used when we don't have polygon boundaries
    point_geom_smerc = models.MultiPointField(srid=3857, null=True, blank=True, editable=False)
    point_geom = models.MultiPointField(srid=4326, null=True, blank=True, editable=False)
    point_geog = models.MultiPointField(srid=4326, geography=True, null=True, blank=True, editable=False)
    
    # Point somewhere within the site
    point_within = models.PointField(srid=4326, null=True, blank=True, editable=False)
    
    # bounding box of polygon
    # assume longitude range is < 180 degrees, bbox can cross dateline
    bbox_lowerleft = models.PointField(srid=4326, null=True, blank=True, editable=False)
    bbox_upperright = models.PointField(srid=4326, null=True, blank=True, editable=False)
    
    # Overriding the default manager with a GeoManager instance
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('mpa-siteinfo', args=[self.pk])
    
    @classmethod
    def get_geom_fields(cls):
        return ('geog', 'geom', 'geom_smerc', 
            'simple_geog', 'simple_geom', 'simple_geom_smerc', 
            'point_geog', 'point_geom', 'point_geom_smerc',
            'point_within', 'bbox_lowerleft', 'bbox_upperright')
    
    @property
    def my_fields(self):
        d = {}
        for field in self._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d

    @property
    def my_fields_list(self):
        return self.my_fields.items()
    
    display_field_names = ('designation', 'designation_type', 'status', 'gov_type',
        'no_take', 'no_take_area', 'rep_m_area', 'fishing', 'fishing_info',
        'access', 'constancy', 'permanence', 'protection_focus',
        'primary_conservation_focus', 'secondary_conservation_focus', 'tertiary_conservation_focus',
        'mgmt_auth', 'mgmt_plan_type', 'mgmt_plan_ref', 'iucn_category', 'int_criteria',
        'mpa_id', 'wdpa_notes', 'notes')
    
    @property
    def display_fields(self):
        d = {}
        for name in self.display_field_names:
            field = self._meta.get_field(name)
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d
    
    @property
    def display_fields_list(self):
        l = []
        for name in self.display_field_names:
            field = self._meta.get_field(name)
            l.append( (name, {"verbose": field.verbose_name, "value": field.value_to_string(self)}) )
        return l

    @property
    def export_field_names(self):
        return mpa_export_fields

    @property
    def export_dict(self):
        export_fields = mpa_export_fields[:] # copy list for local manipulation
        if 'categories' in mpa_export_fields:
            export_fields.remove('categories')
        if 'geom' in export_fields:
            export_fields.remove('geom')
        export_dict = Mpa.objects.filter(pk=self.mpa_id).values(*export_fields).first()
        export_dict = OrderedDict([(f, export_dict[f]) for f in export_fields])
        if 'categories' in mpa_export_fields:
            export_dict['categories'] = list(self.categories.names())
        return export_dict

    @property
    def nation(self):
        try:
            return Nation.objects.get(iso3code=self.country)
        except Nation.DoesNotExist, Nation.MultipleObjectsReturned:
            return None
    
    # Keep ourselves from having to always test if onetoone exists for wikiarticle
    @property
    def get_wikiarticle(self):
        try:
            return self.wikiarticle
        except:
            return None
    
    @transaction.atomic
    def set_point_within(self):
        '''Get a point on the geometry surface.
            Use a point already in the db if possible, otherwise calculate and save one.
        '''
        # Make PostGIS calculate this for us
        try:
            if self.is_point:
                self.point_within = self.point_geom[0] # setting point with first feature in multipoint
            else:
                if not self.geom.valid:
                    return None
                me = self.__class__.objects.point_on_surface(field_name='geom').only('mpa_id').get(pk=self.pk)
                self.point_within = me.point_on_surface
            self.save()
            return self.point_within
        except:
            return None
    
    @transaction.atomic
    def set_bbox(self):
        '''Get the geometry bounding box.
            Use a shape already in the db if possible, otherwise calculate and save one.
        '''
        # This will return a full-width box (-180 to 180) for multipolygons that cross the dateline -- NEED TO FIX
        # Make PostGIS calculate this for us
        try:
            if self.is_point:
                self.bbox_lowerleft = self.point_geom[0] # setting point with first feature in multipoint
                self.bbox_upperright = self.point_geom[0]
            else:
                if not self.geom.valid:
                    return None
                extent = self.__class__.objects.only('mpa_id').filter(pk=self.pk).extent(field_name='geom')
                self.bbox_lowerleft = geos.Point(extent[0], extent[1], srid=gdal.SpatialReference('WGS84').srid)
                self.bbox_upperright = geos.Point(extent[2], extent[3], srid=gdal.SpatialReference('WGS84').srid)
            self.save()
            return (self.bbox_lowerleft, self.bbox_upperright)
        except:
            return None
    
    @transaction.atomic
    def make_point_buffer(self):
        # Raw SQL update geometry fields, much faster than through django
        cursor = connection.cursor()
        cursor.execute("UPDATE mpa_mpa SET simple_geom = ST_Multi("+st_simplify+"(geom, %s)) WHERE mpa_id = %s" , (tolerance, self.mpa_id) )

    @transaction.atomic
    def make_simplified_geom(self, tolerance=0.005, preservetopology=False):
        st_simplify = 'ST_SimplifyPreserveTopology' if preservetopology else 'ST_Simplify'
        # Raw SQL update geometry fields, much faster than through django
        cursor = connection.cursor()
        cursor.execute("UPDATE mpa_mpa SET simple_geom = ST_Multi(ST_MakeValid("+st_simplify+"(geom, %s))) WHERE mpa_id = %s" , (tolerance, self.mpa_id) )

    @transaction.atomic
    def set_geom_from_geog(self):
        # Raw SQL update geometry fields, much faster than through django
        cursor = connection.cursor()
        cursor.execute("UPDATE mpa_mpa SET geom = geog::geometry, geom_smerc = ST_TRANSFORM(geog::geometry, 3857) WHERE mpa_id = %s" , [self.mpa_id])
        cursor.execute("UPDATE mpa_mpa SET point_geom = point_geog::geometry, point_geom_smerc = ST_TRANSFORM(point_geog::geometry, 3857) WHERE mpa_id = %s" , [self.mpa_id])

    @transaction.atomic
    def set_geog_from_geom(self):
        # Raw SQL update geometry fields, much faster than through django
        cursor = connection.cursor()
        cursor.execute("UPDATE mpa_mpa SET geog = geom::geography, geom_smerc = ST_TRANSFORM(geom, 3857) WHERE mpa_id = %s" , [self.mpa_id])
        cursor.execute("UPDATE mpa_mpa SET point_geog = point_geom::geography, point_geom_smerc = ST_TRANSFORM(point_geom, 3857) WHERE mpa_id = %s" , [self.mpa_id])
    
    @transaction.atomic
    @classmethod
    def set_all_geom_from_geog(cls):
        '''A class method to update all geometry rows from geography, affects whole table'''
        cursor = connection.cursor()
        cursor.execute("UPDATE mpa_mpa SET geom = geog::geometry, geom_smerc = ST_TRANSFORM(geog::geometry, 3857)")
        cursor.execute("UPDATE mpa_mpa SET point_geom = point_geog::geometry, point_geom_smerc = ST_TRANSFORM(point_geog::geometry, 3857)")

@receiver(post_save, sender=Mpa)
def mpa_post_save(sender, instance, *args, **kwargs):
    if kwargs['raw']:
        return
    # Calculate things once an mpa object is created or updated
    # Disconnect post_save so we don't enter recursive loop
    post_save.disconnect(mpa_post_save, sender=Mpa)
    try:
        instance.set_point_within()
        instance.set_bbox()
        instance.set_geog_from_geom()
        instance.make_simplified_geom()
    except:
        pass # just move on and stop worrying so much
    finally:
        post_save.connect(mpa_post_save, sender=Mpa)
    try:
        from mpatlas.utils import cartodbmpa
        cartodbmpa.updateMpa(instance.pk)
    except:
        pass # let this fail silently, maybe CartoDB is unreachable


class WikiArticle(models.Model):
    mpa = models.OneToOneField(Mpa, primary_key=True)
    url = models.URLField('Link to Wikipedia Article', null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    summary =  RichTextField('MPA Site Description from Wikipedia', null=True, blank=True)
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.summary[0:20] + '...'
    
    def save(self, *args, **kwargs):
        # Clean up broken html code
        self.summary = BeautifulSoup(self.summary).prettify()
        super(WikiArticle, self).save(*args, **kwargs)


class Contact(models.Model):
    agency = models.CharField(max_length=500)
    url = models.URLField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.agency


class VersionMetadata(models.Model):
    revision = models.OneToOneField(Revision)  # This is required
    comment = models.TextField(blank=True)
    reference = models.TextField(blank=True)

#reversion.register(Mpa)
#reversion.register(WikiArticle)
#reversion.register(Contact)


# class MpaCandidateInfo(models.Model):
#     pass


CANDIDATE_SCOPE_CHOICES = (
    ('Site', 'Site'),
    ('Seascape', 'Seascape'),
)


class CandidateInfo(models.Model):
    mpa = models.OneToOneField(Mpa, primary_key=True)
    summary = RichTextField('Candidate MPA Summary Description', null=True, blank=True)
    
    source = models.CharField(max_length=1000, null=True, blank=True)
    scope = models.CharField(max_length=250, null=True, blank=True, choices=CANDIDATE_SCOPE_CHOICES, default='Site')
    basin = models.CharField(max_length=250, null=True, blank=True)
    region = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
    eez_or_highseas = models.CharField(max_length=1000, null=True, blank=True)
    lead_organization = models.CharField(max_length=500, null=True, blank=True)
    partner_organizations = models.CharField(max_length=1000, null=True, blank=True)
    key_agency_or_leader = models.CharField(max_length=500, null=True, blank=True)
    timeframe = models.CharField(max_length=500, null=True, blank=True)
    current_protection = models.CharField(max_length=1000, null=True, blank=True)
    desired_protection = models.CharField(max_length=1000, null=True, blank=True)
    importance = models.CharField(max_length=1000, null=True, blank=True)
    opportunity = models.CharField(max_length=1000, null=True, blank=True)
    references = models.CharField(max_length=1000, null=True, blank=True)
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return 'Candidate Info: %s' % (self.mpa.name)


class MpaCandidate(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile  
    name = models.CharField(max_length=56)
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPointField(srid=3857, null=True)
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

mpa_export_fields = [
    'mpa_id',
    # 'geom',
    'name',
    'designation',
    'designation_eng',
    'designation_type',
    'access',
    'access_citation',
    'access_info',
    'calc_area',
    'calc_m_area',
    'categories',
    'conservation_effectiveness',
    'conservation_focus_citation',
    'conservation_focus_info',
    'constancy',
    'constancy_citation',
    'contact_id',
    'country',
    'fishing',
    'fishing_citation',
    'fishing_info',
    'gov_type',
    'implementation_date',
    'implemented',
    'int_criteria',
    'is_mpa',
    'is_point',
    'iucn_category',
    'long_name',
    'marine',
    'mgmt_auth',
    'mgmt_plan_ref',
    'mgmt_plan_type',
    'no_take',
    'no_take_area',
    'notes',
    'other_ids',
    'permanence',
    'permanence_citation',
    'primary_conservation_focus',
    'secondary_conservation_focus',
    'tertiary_conservation_focus',
    'protection_focus',
    'protection_focus_citation',
    'protection_focus_info',
    'protection_level',
    'rep_area',
    'rep_m_area',
    'short_name',
    'slug',
    'sovereign',
    'status',
    'status_year',
    'sub_location',
    'summary',
    'usmpa_id',
    'verification_reason',
    'verification_state',
    'verified_by',
    'verified_date',
    'wdpa_id',
    'wdpa_notes'
]

