# -*- coding: utf-8 -*-
# Do not remove, we're using some special characters
# in string literals below

from django.contrib.gis.db import models
from django.contrib.gis import geos, gdal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection, transaction
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from BeautifulSoup import BeautifulSoup
from uuslug import uuslug, slugify

import reversion
from reversion.models import Revision

class Campaign(models.Model):
    # ID / Name
    id = models.AutoField('Campaign id', primary_key=True, editable=False)
    name = models.CharField('Name', max_length=254)
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)

    # Set up foreign key to ISO Countries and Sub Locations
    country = models.CharField('Country / Territory', max_length=20)
    sub_location = models.CharField('Sub Location', max_length=100, null=True, blank=True)
    
    # Summary Info
    summary = RichTextField('Campaign Description', null=True, blank=True)

    # Point location, used when we don't have polygon boundaries
    point_geom = models.PointField(srid=4326, null=True, blank=True, editable=True)

    # Overriding the default manager with a GeoManager instance
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('campaign-info', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = uuslug(self.name, instance=self, separator="_") # optional non-dash separator
        self.slug = uuslug(self.name, instance=self)
        super(Campaign, self).save(*args, **kwargs)


class Initiative(models.Model):
    # ID / Name
    id = models.AutoField('Initiative id', primary_key=True, editable=False)
    name = models.CharField('Name', max_length=254)
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)

    # Summary Info
    summary = RichTextField('Initiative Description', null=True, blank=True)

    # Associated Campaigns
    campaigns = models.ManyToManyField(Campaign)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('initiative-info', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = uuslug(self.name, instance=self, separator="_") # optional non-dash separator
        self.slug = uuslug(self.name, instance=self)
        super(Initiative, self).save(*args, **kwargs)
