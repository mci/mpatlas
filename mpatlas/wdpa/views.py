from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import ListView
from django.db.models import Q
import re
from itertools import chain

#from django.contrib.gis import gdal
from django.contrib.gis import geos, gdal
from django.contrib.gis.measure import Distance

from wdpa.models import WdpaPolygon
from mpa.models import MpaCandidate

class MpaListView(ListView):
    def get_paginate_by(self, queryset):
        try:
            paginate_by = int(self.request.GET.get('paginate_by'))
            if paginate_by > 0:
                return paginate_by
        except:
            pass
        return self.paginate_by
    
    def get_queryset(self):
        try:
            q = self.request.GET.get('q')
            if q:
                #return self.queryset.filter(name__istartswith=q)
                # \m is Postgresql regex word boundary, Python used \b
                # (?i) is a Postgresql regex mode modifier to make regex case insensitive
                return self.queryset.filter(name__regex=r'(?i)\m' + re.escape(q))
        except:
            pass
        else:
            return self.queryset

class MpaJsonListView(MpaListView):
    def render_to_response(self, context, **kwargs):
        return super(MpaJsonListView, self).render_to_response(context, content_type='application/json; charset=utf-8', **kwargs)

def normalize_lon(lon):
    if (not -180 <= lon <= 180):
        lon = lon % 360
        # could also do lon >=180 to cast all 180 to -180
        if (lon > 180):
            lon -= 360
    return lon

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class LookupMethodError(Error):
    """Unknown or malformed spatial lookup method."""
    pass

def lookup_point(request):
    """Find nearby polygons with a point and search radius.
    Three lookup methods are supported:
        sphericalmercator: radius (in km) is applied to search buffer in
            900913 (aka Google Spherical Mercator) projection.  This method
            is appropriate when used in conjuction with web maps.
        greatcircle: uses PostGIS ST_DWithin spatial query on a geography
            column, using great circle distances.
        point: simple test if point is inside polygons (e.g., radius=0)
    These methods assume the geometries are in a Geography column.  Edge
    cases across the dateline are handled correctly.
    Different methods are needed if a regular Geometry column is used
    in order to handle cases across the dateline."""
    mpa_list = ()
    default_method = 'webmercator'
    try:
        lon = float(request.GET['lon'])
        lat = float(request.GET['lat'])
        try:
            radius = float(request.GET['radius'])
        except:
            radius = 225.0 # km
        try:
            method = request.GET['method'] or default_method # set default if empty string passed
        except (KeyError):
            method = default_method
        if method not in ('point', 'greatcircle', 'webmercator', 'webmercator_buffer', 'webmercator_box', 'webmercator_simple'):
            raise LookupMethodError('Unknown or malformed lookup method passed in GET query string.')
        if (radius == 0):
            method = 'point'
    except:
        # Bad input, return empty list
        return render_to_response('wdpa/mpalookup.json', {
            'mpalist': mpa_list,
        }, context_instance=RequestContext(request))
    else:
        # We need to normalize the longitude into the range -180 to 180 so we don't
        # make the cast to PostGIS Geography type complain
        point = geos.Point(normalize_lon(lon), lat, srid=gdal.SpatialReference('WGS84').srid) # srid=4326 , WGS84 geographic
        if (method == 'webmercator'):
            if (normalize_lon(lon) < 0):
                lon360 = normalize_lon(lon) + 360
            else:
                lon360 = normalize_lon(lon) - 360
            point360 = geos.Point(lon360, lat, srid=gdal.SpatialReference('WGS84').srid)
            point.transform(900913) # Google Spherical Mercator srid
            point360.transform(900913)
            #mpa_list = WdpaPolygon.objects.filter(geom_smerc__dwithin=(point, Distance(km=radius))).defer(*WdpaPolygon.get_geom_fields())
            mpa_list = WdpaPolygon.objects.filter(Q(geom_smerc__dwithin=(point, Distance(km=radius))) | Q(geom_smerc__dwithin=(point360, Distance(km=radius)))).defer(*WdpaPolygon.get_geom_fields())
            search = point
        elif (method == 'webmercator_buffer'):
            point.transform(900913) # Google Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000) # convert km to m, create buffer
            mpa_list = WdpaPolygon.objects.filter(geog__intersects=searchbuffer).defer(*WdpaPolygon.get_geom_fields())
            search = searchbuffer
        elif (method == 'webmercator_box'):
            point.transform(900913) # Google Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000)
            mpa_list = WdpaPolygon.objects.filter(geog__intersects=searchbuffer.envelope).defer(*WdpaPolygon.get_geom_fields()) # use simple bounding box instead
            search = searchbuffer.envelope
        elif (method == 'webmercator_simple'):
            point.transform(900913) # Google Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000, quadsegs=2) # simple buffer with 2 segs per quarter circle
            mpa_list = WdpaPolygon.objects.filter(geog__intersects=searchbuffer).defer(*WdpaPolygon.get_geom_fields())
            search = searchbuffer
        elif (method == 'greatcircle'):
            mpa_list = WdpaPolygon.objects.filter(geog__dwithin=(point, Distance(km=radius))).defer(*WdpaPolygon.get_geom_fields())
            search = point
        elif (method == 'point'):
            mpa_list = WdpaPolygon.objects.filter(geog__intersects=point).defer(*WdpaPolygon.get_geom_fields())
            search = point
        mpa_candidate_list = MpaCandidate.objects.filter(geog__dwithin=(point, Distance(km=radius))).defer('geog')
        search.transform(4326)
        return render_to_response('wdpa/mpalookup.json', {
            'search': search.coords,
            'mpa_list': mpa_list,
            'mpa_candidate_list': mpa_candidate_list,
        }, context_instance=RequestContext(request))