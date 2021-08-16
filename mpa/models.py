# -*- coding: utf-8 -*-
# Do not remove, we're using some special characters
# in string literals below

from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis import geos, gdal
from django.dispatch import receiver
from django.db import connection, transaction
from django.db.models import F, Func
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
try:
    # Django >= 3.0
    from django.contrib.gis.db.models import JSONField
except:
    # Django < 3.0
    from django.contrib.postgres.fields import JSONField
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup

# import reversion
from reversion import revisions as reversion
from reversion.models import Revision

from taggit.managers import TaggableManager
from category.models import TaggedItem

from django.contrib.gis.db.models import Extent
from django.contrib.gis.db.models.functions import IsValid, MakeValid

from spatialdata.models import Nation

from collections import OrderedDict

from filer.fields.image import FilerImageField

import logging
logger = logging.getLogger('mpa')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

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

VERIFY_WDPA_CHOICES = (
    ('Not Reported', 'Not Reported'),
    ('State Verified', 'State Verified'),
    ('Expert Verified', 'Expert Verified'),
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
 
OWN_TYPE_CHOICES = (
    ('State', 'State'),
    ('Communal', 'Communal'),
    ('Individual landowners', 'Individual landowners'),
    ('For-profit organisations', 'For-profit organisations'),
    ('Non-profit organisations', 'Non-profit organisations'),
    ('Joint ownership', 'Joint ownership'),
    ('Multiple ownership', 'Multiple ownership'),
    ('Contested', 'Contested'),
    ('Not Reported', 'Not Reported'),
)

STATUS_CHOICES = (
    ('Proposed', 'Proposed'),
    # ('Adopted', 'Adopted'),
    # ('Inscribed', 'Inscribed'),
    ('Designated', 'Designated'),
    ('Defunct/Degazetted', 'Defunct/Degazetted'),
)

GLORES_CHOICES = (
    ('', 'None'),
    ('nominee', 'Nominee'),
    ('platinum', 'Platinum Award'),
    ('gold', 'Gold Award'),
    ('silver', 'Silver Award'),
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
    ('Not Applicable','Not Applicable'),
)

PROTECTION_LEVEL_CHOICES = (
    ('full', 'Fully Protected'),
    ('high', 'Highly Protected'),
    ('light', 'Lightly Protected'),
    ('minimal', 'Minimally Protected'),
    ('incompatible', 'Incompatible with MPA Conservation Goals'),
    ('unknown', 'Unknown'),
)

FISHING_PROTECTION_LEVEL_CHOICES = PROTECTION_LEVEL_CHOICES
PROTECTION_LEVEL_MPAGUIDE_CHOICES = PROTECTION_LEVEL_CHOICES

rbcs1_levels = {
    1: 'No-Take/No-Go',
    2: 'No-Take/Regulated Access',
    3: 'No-Take/Unregulated Access',
    4: 'Highly Regulated Extraction',
    5: 'Moderately Regulated Extraction',
    6: 'Weakly Regulated Extraction',
    7: 'Very Weakly Regulated Extraction',
    8: 'Unregulated Extraction',
    99: 'Unknown'
}

PROTECTION_LEVEL_RBCS_CHOICES = [(i, '%d: %s' % (i,j)) for (i,j) in rbcs1_levels.items()]
PROTECTION_LEVEL_RBCS_NAME_CHOICES = [(j.lower(),j) for j in rbcs1_levels.values()]

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

MARINE_CHOICES = (
    (0, '0 - Not Marine/Unknown'),
    (1, '1 - Coastal/Part Marine'),
    (2, '2 - Full Marine'),
)


class Site(models.Model):
    # ID / Name
    site_id = models.AutoField('MPA Site ID', primary_key=True, editable=False)
    wdpa_id = models.IntegerField('WDPA ID', null=True, blank=True, help_text='WDPA ID code.')
    usmpa_id = models.CharField('US MPA ID', max_length=50, null=True, blank=True, help_text='US NOAA MPA Center ID. You probably should not be changing this.')
    other_ids = models.CharField('Other reference id codes', max_length=1000, null=True, blank=True, help_text='ID codes used by other groups to identify this area, e.g., TNC Caribbean or Coral Triangle Atlas ids.')
    name = models.CharField('Name', max_length=254, blank=True, help_text='Protected area site name not including designation title')
    orig_name = models.CharField('Original Name', max_length=254, blank=True, default='', help_text='Protected area original site name not including designation title')
    short_name = models.CharField(max_length=254, blank=True, help_text='Nickname if any') # name + designation with abbreviations
    slug = models.CharField('URL Slug', max_length=254, blank=True, help_text='URL slug string')

    designation = models.CharField('Designation', max_length=254, null=True, blank=True)
    designation_eng = models.CharField('English Designation', max_length=254, null=True, blank=True)

    # Taggit TaggableManger used to define categories
    categories = TaggableManager(through=TaggedItem, verbose_name='Categories', help_text='You can assign this site to one or more categories by providing a comma-separated list of tags enclosed in quotes (e.g., [ "Shark Sanctuary", "World Heritage Site" ]', blank=True)
    glores_status = models.CharField('GLORES Status', max_length=100, blank=True, choices=GLORES_CHOICES, default='')

    # Summary Info
    summary = RichTextField('MPA Summary Site Description', null=True, blank=True)

    # Returns the string representation of the model.
    def __str__(self):
        return "[%s] %s - %s" % (self.site_id, self.name, self.designation_eng)

    # def get_absolute_url(self):
    #     return reverse('mpa-siteinfo', args=[self.pk])



class Mpa(models.Model):
    # ID / Name
    mpa_id = models.AutoField('MPA ID', primary_key=True, editable=False)
    wdpa_id = models.IntegerField('WDPA ID', null=True, blank=True, help_text='WDPA ID code. You probably should not be changing this.')
    wdpa_pid = models.CharField('WDPA Parcel ID', max_length=52, null=True, blank=True, help_text='WDPA Parcel ID code in form wdpaid_X. You probably should not be changing this.')
    usmpa_id = models.CharField('US MPA ID', max_length=50, null=True, blank=True, help_text='US NOAA MPA Center ID. You probably should not be changing this.')
    other_ids = models.CharField('Other reference id codes', max_length=1000, null=True, blank=True, help_text='ID codes used by other groups to identify this area, e.g., TNC Caribbean or Coral Triangle Atlas ids.')
    name = models.CharField('Name', max_length=254, help_text='Protected area name not including designation title')
    orig_name = models.CharField('Original Name', max_length=254, blank=True, default='', help_text='Protected area original name not including designation title')
    long_name = models.CharField(max_length=254, blank=True) # name + designation
    short_name = models.CharField(max_length=254, blank=True, help_text='Nickname if any') # name + designation with abbreviations
    slug = models.CharField(max_length=254, blank=True)

    site = models.ForeignKey('Site', related_name='zones', related_query_name='zone', verbose_name='MPA Parent Site', null=True, blank=True, on_delete=models.SET_NULL)

    # Taggit TaggableManger used to define categories
    categories = TaggableManager(through=TaggedItem, verbose_name='Categories', help_text='You can assign this area to one or more categories by providing a comma-separated list of tags enclosed in quotes (e.g., [ "Shark Sanctuary", "World Heritage Site" ]', blank=True)
    glores_status = models.CharField('GLORES Status', max_length=100, blank=True, choices=GLORES_CHOICES, default='')

    # Set up foreign key to ISO Countries and Sub Locations
    sovereign = models.CharField('Sovereign Country', max_length=50, null=True, blank=True)
    country = models.CharField('Country / Territory', max_length=50)
    sub_location = models.CharField('Sub Location', max_length=100, null=True, blank=True)
    
    # Verification State
    is_mpa = models.BooleanField('MPAtlas MPA Definition', default=True)
    pa_def = models.BooleanField('Protected Area Definition', default=True)
    verification_state = models.CharField('Verification State', max_length=100, default='Unverified', choices=VERIFY_CHOICES)
    verification_reason = models.CharField('Verification Reason', max_length=1000, null=True, blank=True)
    verified_by = models.CharField('Verified By', max_length=100, null=True, blank=True)
    verified_date = models.DateField('Date Verified', null=True, blank=True)
    verify_wdpa = models.CharField('Verification by WDPA', max_length=20, null=True, blank=True, default='Not Reported', choices=VERIFY_WDPA_CHOICES)

    # Data Sources
    datasources = JSONField('Data Sources', default=dict, editable=True)
    '''EXAMPLE
        {
            'attributes': [{'name': “WDPA”, 'version': "2020-12", 'url': "", 'notes':""}],
            'geospatial': [{'name': "MPAtlas/MCI", version: "", 'url':"", 'notes':""}],
            'metadata': ""
        }
    '''
    wdpa_metadataid = models.IntegerField('WDPA Source Metadata ID', null=True, blank=True, editable=False)

    # Modification History
    created_date = models.DateTimeField('Creation Date', help_text='Date and time record created', auto_now_add=True, null=True)
    modified_date = models.DateTimeField('Modification Date', help_text='Date and time of last record save', auto_now=True, null=True)
    
    # Designation
    designation = models.CharField('Designation', max_length=254, null=True, blank=True)
    designation_eng = models.CharField('English Designation', max_length=254, null=True, blank=True)
    designation_type = models.CharField('Designation Type', max_length=20, null=True, blank=True, choices=DESIG_TYPE_CHOICES)
    iucn_category = models.CharField('IUCN Category', max_length=20, null=True, blank=True, choices=IUCN_CAT_CHOICES)
    int_criteria = models.CharField('International Criteria', max_length=100, null=True, blank=True)
    marine = models.IntegerField('Marine (field from WDPA)', null=True, default=0, choices=MARINE_CHOICES)
    status = models.CharField('Status', max_length=100, null=True, blank=True, choices=STATUS_CHOICES, default='Designated')
    status_year = models.IntegerField('Status Year', null=True, blank=True)
    status_mpatlas = models.CharField('Status (mpatlas value)', max_length=100, null=True, blank=True, choices=STATUS_CHOICES, default='Designated')
    status_year_mpatlas = models.IntegerField('Status Year (mpatlas value)', null=True, blank=True)

    # Implementation
    # establishment_stage = proposed, designated, implemented, actively_managed
    implemented = models.BooleanField('Implemented?', help_text='MPA is designated and implemented with regulations enforced', blank=True, default=True)
    implementation_date = models.DateField('Implementation Date', help_text='Date regulations went into effect or will go into effect', null=True, blank=True)
    
    # Area Estimates
    no_take = models.CharField('No Take', max_length=100, choices=NO_TAKE_CHOICES, default='Not Reported')
    no_take_area = models.FloatField('No Take Area km²', null=True, blank=True)
    rep_m_area = models.FloatField('Reported Marine Area km²', null=True, blank=True)
    calc_m_area = models.FloatField('Calculated Marine Area km²', null=True, blank=True)
    rep_area = models.FloatField('Reported Area km²', null=True, blank=True)
    calc_area = models.FloatField('Calculated Area km²', null=True, blank=True)

    no_take_wdpa = models.CharField('No Take (wdpa value)', max_length=100, choices=NO_TAKE_CHOICES, default='Not Reported')
    no_take_area_wdpa = models.FloatField('No Take Area km² (wdpa value)', null=True, blank=True)
    no_take_mpatlas = models.CharField('No Take (mpatlas value)', max_length=100, choices=NO_TAKE_CHOICES, default='Not Reported')
    no_take_area_mpatlas = models.FloatField('No Take Area km² (mpatlas value)', null=True, blank=True)
    calc_m_area_mpatlas = models.FloatField('Calculated Marine Area km² (mpatlas value)', null=True, blank=True)
    calc_area_mpatlas = models.FloatField('Calculated Area km² (mpatlas value)', null=True, blank=True)
    
    # Management details
    gov_type = models.CharField('Governance Type', max_length=254, null=True, blank=True) # = US gov_level
    own_type = models.CharField('Ownership Type', max_length=254, null=True, blank=True, choices=OWN_TYPE_CHOICES, default='State') # WDPA OWN_TYPE
    mgmt_auth = models.CharField('Management Authority', max_length=254, null=True, blank=True)
    mgmt_plan_type = models.CharField('Management Plan Type', max_length=254, null=True, blank=True)
    mgmt_plan_ref = models.CharField('Management Plan Reference', max_length=254, null=True, blank=True)
    
    # Contact
    contact = models.ForeignKey('Contact', related_name='mpa_main_set', verbose_name='Main Contact', null=True, blank=True, on_delete=models.SET_NULL)
    other_contacts = models.ManyToManyField('Contact', verbose_name='Other Contacts', blank=True)
    
    #Conservation Effectiveness
    conservation_effectiveness = models.CharField(max_length=254, null=True, blank=True, choices=CONSERVATION_EFFECTIVENESS_CHOICES, default='Unknown')

    # FISHING PROTECTION LEVEL
    fishing_protection_level = models.CharField('Fishing Protection Level', max_length=100, default='unknown', blank=True, choices=FISHING_PROTECTION_LEVEL_CHOICES, editable=False)
    fishing_protection_details = JSONField('Fishing Protection Level Details', default=dict, editable=False)
    '''EXAMPLE
        {
            'method': 'MPA Guide | RBCS | No-Take',
            'level': 'full | high | light | minimal | incompatible | unknown',
            'complete': 'complete | incomplete',
            'assessment_date': '2020-10-22 | None'
        }
    '''

    # PROTECTION LEVEL
    protection_mpaguide_level = models.CharField('Protection Level - MPA Guide', max_length=100, default='unknown', blank=True, choices=PROTECTION_LEVEL_MPAGUIDE_CHOICES, editable=False)
    protection_mpaguide_details = JSONField('Protection Level Details - MPA Guide', default=dict, editable=False)
    '''EXAMPLE
        {
            'version': '1.0',
            'level': 'full | high | light | minimal | incompatible | unknown', # if incomplete, highest level allowed
            'complete': 'complete | incomplete',
            'assessment_date': '2020-10-22',
            'publish_status': 'draft | review | published | rejected',
            'classes': {
                'mining': {
                    'level': 'full | incompatible | unknown',
                    'value': 'no | yes | unknown'
                },
                'dredging_dumping': {
                    'level': 'full | light | incompatible | unknown',
                    'value': 'no | yes, selective | yes, incompatible | yes | unknown'
                },
                'anchoring': {
                    'level': 'full | high | light | minimal | incompatible | unknown',
                    'value': 'no impact | minimal impact | low impact | moderate impact | large impact | incompatible with conservation | unknown'
                },
                'infrastructure': {
                    'level': 'full | high | light | minimal | incompatible | unknown',
                    'value': 'minimal impact | low impact | moderate impact | large impact | incompatible with conservation | unknown'
                },
                'aquaculture': {
                    'level': 'full | high | light | minimal | incompatible | unknown',
                    'value': 'no | low impact | moderate impact | large impact | incompatible with conservation | unknown'
                },
                'fishing_extraction': {
                    'level': 'full | high | light | minimal | incompatible | unknown',
                    'value': 'no | low impact | moderate impact | large impact | incompatible with conservation | unknown'
                },
                'nonextractive_activities': {
                    'level': 'full | high | light | unknown',
                    'value': 'minimal impact | low impact | unregulated or high impact | unknown'
                }
            }
        }
    '''

    # 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 99=unknown
    # Should we change this to be 1-8 and null for unknown instead of using 99?
    protection_rbcs_level = models.IntegerField('Protection Level - RBCS', default=99, blank=True, choices=PROTECTION_LEVEL_RBCS_CHOICES, editable=False)
    # no-take / no-go | no-take / unregulated access | highly regulated extraction | moderately regulated extraction | weakly regulated extraction | very weakly regulated extraction | unregulated extraction | unknown
    protection_rbcs_level_name = models.CharField('Protection Level Name - RBCS', max_length=100, default='unknown', blank=True, choices=PROTECTION_LEVEL_RBCS_NAME_CHOICES, editable=False)
    protection_rbcs_details = JSONField('Protection Level Details - RBCS', default=dict, editable=False)
    '''EXAMPLE
        {
            'version': '1 | 2.1',
            'level': 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 99,
            'level_name': 'no-take/no-go | no-take/regulated access | no-take/unregulated access | highly regulated extraction | moderately regulated extraction | weakly regulated extraction | very weakly regulated extraction | unregulated extraction | unknown',
            'range': [max_level_allowed, min_level_allowed], # if incomplete, possible range of values allowed given partial inputs
            'complete': 'complete | incomplete',
            'assessment_date': '2020-10-22',
            'publish_status': 'draft | review | published | rejected',
            'classes': {
                'aquaculture_bottom_exploitation_index': 0 | 1 | 2 | null,
                'recreational_access_index': 0 | 1 | 2 | null,
                'num_gears': 0-99 | null,
                'max_gear_score': 0-9 | null
            }
        }
    '''

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

    # WDPA Additional Fields
    supp_info_wdpa = models.CharField(max_length=254, null=True, blank=True)
    cons_obj_wdpa = models.CharField(max_length=100, null=True, blank=True)
    
    # Summary Info
    summary = RichTextField('MPA Summary Zone Description', null=True, blank=True)
    
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

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    def get_absolute_url(self):
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
        return list(self.my_fields.items())
    
    display_field_names = ('name', 'orig_name', 'designation', 'designation_eng', 'designation_type',
        'status', 'status_year', 'is_mpa', 'implemented', 'mpa_id', 'wdpa_id', 'wdpa_pid',
        'iucn_category', 'no_take', 'no_take_area', 'rep_m_area', 'rep_area', 'fishing', 'fishing_info',
        'access', 'constancy', 'permanence',
        'gov_type', 'mgmt_auth', 'own_type', 'mgmt_plan_type', 'mgmt_plan_ref',  'int_criteria',
    )
    
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
        except (Nation.DoesNotExist, Nation.MultipleObjectsReturned) as e:
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
                extent = self.__class__.objects.only('mpa_id').filter(pk=self.pk).aggregate(Extent('geom')).get('geom__extent')
                self.bbox_lowerleft = geos.Point(extent[0], extent[1], srid=gdal.SpatialReference('WGS84').srid)
                self.bbox_upperright = geos.Point(extent[2], extent[3], srid=gdal.SpatialReference('WGS84').srid)
            self.save()
            return (self.bbox_lowerleft, self.bbox_upperright)
        except:
            return None
    
    @transaction.atomic
    def clean_geom(self, resolution=1e-09, dry_run=False):
        '''Clean geometry by running ST_MakeValid and ST_RemoveRepeatedPoints.
        Uses default decimal degree resolution/tolerance of 1E-09 (~0.1mm),
        which is default geodatabase XY Resolution in ArcGIS.'''
        fixed = False
        mpaset = Mpa.objects.filter(pk=self.mpa_id).annotate(geom_nodup=MakeValid(Func(F('geom'), resolution, function='ST_RemoveRepeatedPoints')))
        # Run MakeValid first if not valid, doing this on a query set rather than object
        mpa = mpaset.first()
        invalid = mpaset.annotate(valid=IsValid('geom')).filter(valid=False)
        if invalid.exists():
            if not dry_run:
                invalid.update(geom=MakeValid('geom'))
            # save object at end of function to invoke triggers only if geom was actually updated
            logger.warning('Fixed Invalid Geometry: mpa_id %s %s %s %s', mpa.mpa_id, mpa.name, mpa.designation, mpa.country)
            fixed = True
        # Remove duplicate points at 1e-09 resolution (ArcGIS default), even though PostGIS is differentiating at 15 decimal places
        # Run MakeValid on resulting geom without duplicates just to be safe
        if (mpa.geom and mpa.geom_nodup.num_coords < mpa.geom.num_coords):
            # Test for mpa.geom above ensures we don't run this on a null geometry
            logger.warning('Removed %d Duplicate Points: mpa_id %s %s %s %s', mpa.geom.num_coords - mpa.geom_nodup.num_coords, mpa.mpa_id, mpa.name, mpa.designation, mpa.country)
            mpa.geom = mpa.geom_nodup 
            fixed=True
        if fixed and not dry_run:
            mpa.save() # save rather than SQL update so Django triggers fire
            # Because mpa.clean_geom() is in the post_save trigger, this routine probably runs twice
            # when errors are fixed if clean_geom is called on its own.
        return fixed

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
        instance.clean_geom()
        instance.set_point_within()
        instance.set_bbox()
        instance.set_geog_from_geom()
        instance.make_simplified_geom()
    except:
        pass # just move on and stop worrying so much
    finally:
        post_save.connect(mpa_post_save, sender=Mpa)
    try:
        from mpatlas.utils import cartompa
        cartompa.updateMpa(instance.pk)
    except:
        pass # let this fail silently, maybe Carto is unreachable

@receiver(post_delete, sender=Mpa)
def mpa_post_delete(sender, instance, *args, **kwargs):
    try:
        from mpatlas.utils import cartompa
        cartompa.purgeCartoMpas()
    except:
        pass # let this fail silently, maybe Carto is unreachable


class WikiArticle(models.Model):
    mpa = models.OneToOneField(Mpa, primary_key=True, on_delete=models.CASCADE)
    url = models.URLField('Link to Wikipedia Article', null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    summary =  RichTextField('MPA Site Description from Wikipedia', null=True, blank=True)
    
    # Returns the string representation of the model.
    def __str__(self):
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
    logo = FilerImageField(null=True, blank=True, related_name="contact_logos", on_delete=models.SET_NULL)
    
    # Returns the string representation of the model.
    def __str__(self):
        return 'Contact: %s' % (self.agency)

# class DataSource(models.Model):
#     name = models.CharField('Data Source Name', max_length=500)
#     version = models.CharField('Version or Access Date', max_length=500, null=True, blank=True)
#     url = models.URLField('Data Source URL', max_length=500, null=True, blank=True)
#     logo = FilerImageField(null=True, blank=True, related_name="datasource_logos", on_delete=models.SET_NULL)
        
#     # Returns the string representation of the model.
#     def __str__(self):
#         return 'Data Source: %s - %s' % (self.name, self.version)


class VersionMetadata(models.Model):
    revision = models.OneToOneField(Revision, on_delete=models.CASCADE)  # This is required
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
    mpa = models.OneToOneField(Mpa, primary_key=True, on_delete=models.CASCADE)
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
    def __str__(self):
        return 'Candidate Info: %s' % (self.mpa.name)


class MpaCandidate(models.Model):
    # Regular fields corresponding to attributes in wdpa shpfile  
    name = models.CharField(max_length=56)
    
    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom_smerc = models.MultiPointField(srid=3857, null=True)
    geom = models.MultiPointField(srid=4326, null=True)
    geog = models.MultiPointField(srid=4326, geography=True, null=True)
    
    # Returns the string representation of the model.
    def __str__(self):
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
        return sorted(list(self.myfields.items()))

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
    'fishing_protection_level',
    'fishing_protection_details',
    'gov_type',
    'glores_status',
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
    'pa_def',
    'permanence',
    'permanence_citation',
    'primary_conservation_focus',
    'secondary_conservation_focus',
    'tertiary_conservation_focus',
    'protection_focus',
    'protection_focus_citation',
    'protection_focus_info',
    'protection_mpaguide_level',
    'protection_mpaguide_details',
    'protection_rbcs_level',
    'protection_rbcs_level_name',
    'protection_rbcs_details',
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
    'verify_wdpa',
    'verification_reason',
    'verification_state',
    'verified_by',
    'verified_date',
    'wdpa_id',
    'wdpa_notes',
    'supp_info_wdpa',
    'cons_obj_wdpa',
]

