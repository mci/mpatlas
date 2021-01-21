# -*- coding: utf-8 -*-
# Do not remove, we're using some special characters
# in string literals below

from django.contrib.gis.db import models
from django.contrib.gis import geos, gdal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connection, transaction
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
from uuslug import uuslug, slugify
import datetime

# import reversion
from reversion import revisions as reversion
from reversion.models import Revision

from mpa.models import Mpa
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager
from category.models import TaggedItem


# fields variable is overwritten at end of module, listing all fields needed to pull from mpatlas
# via a .values(*fields) call.  Update this for new columns.
campaign_export_fields = []

YEAR_CHOICES = [(None, None)] + [(r,r) for r in range(1990, datetime.date.today().year+1)]

class Campaign(models.Model):
    # ID / Name
    id = models.AutoField('Campaign id', primary_key=True, editable=False)
    name = models.CharField('Name', max_length=254)
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)

    # Taggit TaggableManger used to define categories
    categories = TaggableManager(through=TaggedItem, verbose_name='Categories', help_text='You can assign this area to one or more categories by providing a comma-separated list of tags (e.g., [ Shark Sanctuary, World Heritage Site ]', blank=True)

    # Set up foreign key to ISO Countries and Sub Locations
    country = models.CharField('Country / Territory', max_length=20)
    sub_location = models.CharField('Sub Location', max_length=100, null=True, blank=True)
    
    # Summary Info
    logo = FilerImageField(verbose_name='Campaign Logo', related_name='campaign_logos', blank=True, null=True, on_delete=models.SET_NULL)
    summary = RichTextField('Campaign Description', null=True, blank=True)

    # Associated Organizations
    organizations = models.ManyToManyField('Organization')

    # Associated MPAs
    mpas = models.ManyToManyField(Mpa, blank=True)

    # Point location, used when we don't have polygon boundaries
    is_point = models.BooleanField(default=False)
    point_geom = models.PointField(srid=4326, null=True, blank=True, editable=False)
    point_geom_smerc = models.PointField(srid=3857, null=True, blank=True, editable=False)
    
    # Full-res polygon features
    # If is_point is true, this will be a box or circle based on the 
    # area estimate (calculated from local UTM crs or a global equal area crs)
    geom = models.MultiPolygonField(srid=4326, null=True, blank=True, editable=False)
    geom_smerc = models.MultiPolygonField(srid=3857, null=True, blank=True, editable=False)

    # Campaign Status
    start_year = models.IntegerField(_('Start Year'), choices=YEAR_CHOICES, null=True, blank=True)
    active = models.BooleanField(default=True)

    # Associated MPAs
    mpas = models.ManyToManyField(Mpa, blank=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('campaign-info', args=[self.slug])

    @classmethod
    def get_geom_fields(cls):
        return ('geom', 'geom_smerc', 'point_geom')

    @property
    def my_fields(self):
        d = {}
        for field in self._meta.fields:
            d[field.name] = { "verbose": field.verbose_name, "value": field.value_to_string(self) }
        return d

    @property
    def my_fields_list(self):
        return list(self.my_fields.items())

    @property
    def export_field_names(self):
        return campaign_export_fields

    @property
    def export_dict(self):
        export_fields = campaign_export_fields[:] # copy list for local manipulation
        if 'categories' in campaign_export_fields:
            export_fields.remove('categories')
        if 'mpas' in campaign_export_fields:
            export_fields.remove('mpas')
        if 'geom' in export_fields:
            export_fields.remove('geom')
        if 'point_geom' in export_fields:
            export_fields.remove('geom')
        export_dict = Campaign.objects.filter(pk=self.id).values(*export_fields).first()
        export_dict = OrderedDict([(f, export_dict[f]) for f in export_fields])
        if 'categories' in campaign_export_fields:
            export_dict['categories'] = list(self.categories.names())
        if 'mpas' in campaign_export_fields:
            export_dict['mpas'] = list(campaign.mpas.values_list('pk', flat=True))
        return export_dict

    @transaction.atomic
    def process_geom_fields(self):
        # Raw SQL update geometry fields, much faster than through django
        cursor = connection.cursor()
        cursor.execute("UPDATE campaign_campaign SET geom_smerc = ST_TRANSFORM(geom, 3857) WHERE id = %s" , [self.id])
        cursor.execute("UPDATE campaign_campaign SET point_geom_smerc = ST_TRANSFORM(point_geom, 3857) WHERE id = %s" , [self.id])
        self.is_point = False if self.geom else True
        self.save()

    def save(self, *args, **kwargs):
        # self.slug = uuslug(self.name, instance=self, separator="_") # optional non-dash separator
        if not self.slug:
            # set slug from name only if slug is empty
            self.slug = uuslug(self.name, instance=self)
        else:
            # set slug from what was given in slug field
            # if slug previously set and unique, just return the same slug
            # if slug is not unique, append integer (e.g. '-1')
            self.slug = uuslug(self.slug, instance=self)
        super(Campaign, self).save(*args, **kwargs)

@receiver(post_save, sender=Campaign)
def campaign_post_save(sender, instance, *args, **kwargs):
    if kwargs['raw']:
        return
    # Calculate things once an mpa object is created or updated
    # Disconnect post_save so we don't enter recursive loop
    post_save.disconnect(campaign_post_save, sender=Campaign)
    try:
        instance.process_geom_fields()
    except:
        pass # just move on and stop worrying so much
    finally:
        post_save.connect(campaign_post_save, sender=Campaign)
    try:
        from mpatlas.utils import cartompa
        cartompa.updateCampaign(instance.pk)
    except:
        pass # let this fail silently, maybe Carto is unreachable

@receiver(post_delete, sender=Campaign)
def campaign_post_delete(sender, instance, *args, **kwargs):
    # Calculate things once an mpa object is created or updated
    # Disconnect post_save so we don't enter recursive loop
    try:
        from mpatlas.utils import cartompa
        cartompa.purgeCartoCampaigns()
    except:
        pass # let this fail silently, maybe Carto is unreachable


class Initiative(models.Model):
    # ID / Name
    id = models.AutoField('Initiative id', primary_key=True, editable=False)
    name = models.CharField('Name', max_length=254)
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)

    # Summary Info
    logo = FilerImageField(verbose_name='Initiative Logo', related_name='initiative_logos', blank=True, null=True, on_delete=models.SET_NULL)
    summary = RichTextField('Initiative Description', null=True, blank=True)

    # Associated Campaigns
    campaigns = models.ManyToManyField(Campaign)

    # Associated Organizations
    organizations = models.ManyToManyField('Organization')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('initiative-info', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = uuslug(self.name, instance=self, separator="_") # optional non-dash separator
        if not self.slug:
            # set slug from name only if slug is empty
            self.slug = uuslug(self.name, instance=self)
        else:
            # set slug from what was given in slug field
            # if slug previously set and unique, just return the same slug
            # if slug is not unique, append integer (e.g. '-1')
            self.slug = uuslug(self.slug, instance=self)
        super(Initiative, self).save(*args, **kwargs)


class Organization(models.Model):
    # ID / Name
    id = models.AutoField('Organization id', primary_key=True, editable=False)
    name = models.CharField('Name', max_length=254)
    nickname = models.CharField('Nickname or Acronym', max_length=254)
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)

    # Summary Info
    logo = FilerImageField(verbose_name='Organization Logo', related_name='organization_logos', blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField('Website', max_length=254, blank=True)
    social_handles = models.CharField('Social Media Handles', max_length=254, blank=True)
    summary = RichTextField('Organization Description', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('org-info', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = uuslug(self.name, instance=self, separator="_") # optional non-dash separator
        if not self.slug:
            # set slug from name only if slug is empty
            self.slug = uuslug(self.name, instance=self)
        else:
            # set slug from what was given in slug field
            # if slug previously set and unique, just return the same slug
            # if slug is not unique, append integer (e.g. '-1')
            self.slug = uuslug(self.slug, instance=self)
        super(Organization, self).save(*args, **kwargs)

campaign_export_fields = [
    'id',
    'name',
    'slug',
    'categories',
    'country',
    'sub_location',
    'summary',
    'is_point',
    'start_year',
    'active',
    'mpas',
    #'point_geom',
    #'geom',
]
