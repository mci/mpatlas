from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
import re

from django.views.generic import ListView
from mpa.views import MpaListView, MpaJsonListView

from django.contrib.gis import geos, gdal
from django.contrib.gis.measure import Distance

from spatialdata.models import Eez, Nation

class EezListView(MpaListView):    
    def get_queryset(self):
        try:
            q = self.request.GET.get('q')
            if q:
                #return self.queryset.filter(name__istartswith=q)
                # \m is Postgresql regex word boundary, Python used \b
                # (?i) is a Postgresql regex mode modifier to make regex case insensitive
                return self.queryset.filter(eez__regex=r'(?i)\m' + re.escape(q))
        except:
            pass
        else:
            return self.queryset

class EezJsonListView(EezListView):
    def render_to_response(self, context, **kwargs):
        return super(EezJsonListView, self).render_to_response(context, content_type='application/json; charset=utf-8', **kwargs)

def get_geom_wkt(request, model, pk, simplified=True, webmercator=False):
    geomfield = 'geom'
    if (webmercator):
        geomfield = 'geom_smerc'
    if simplified:
        geomfield = 'simple_' + geomfield
    obj = model.objects.only(geomfield).get(pk=pk)
    return HttpResponse(getattr(obj,geomfield).wkt, content_type='text/plain; charset=utf-8')

def get_geom_json(request, model, pk, simplified=True, webmercator=False):
    try:
        simplified = (not request.GET['simplified'].upper() == 'FALSE')
    except:
        pass
    try:
        webmercator = (request.GET['webmercator'].upper() == 'TRUE')
    except:
        pass
    geomfield = 'geom'
    if (webmercator):
        geomfield = 'geom_smerc'
    if simplified:
        geomfield = 'simple_' + geomfield
    obj = model.objects.geojson(field_name=geomfield).defer(*model.get_geom_fields()).get(pk=pk)
    return HttpResponse(obj.geojson, content_type='application/json; charset=utf-8')

def get_nation_geom_json(request, iso3code, simplified=True, webmercator=False):
    try:
        simplified = (not request.GET['simplified'].upper() == 'FALSE')
    except:
        pass
    try:
        webmercator = (request.GET['webmercator'].upper() == 'TRUE')
    except:
        pass
    geomfield = 'geom'
    if (webmercator):
        geomfield = 'geom_smerc'
    if simplified:
        geomfield = 'simple_' + geomfield
    try:
        n = Nation.objects.get(iso3code=iso3code)
    except Nation.DoesNotExist:
        n = None
    # geojson = n.eez_set.all().collect(field_name=geomfield).geojson
    geojson = n.geom.geojson
    return HttpResponse(geojson, content_type='application/json; charset=utf-8')

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

def region_lookup_point(request, region):
    """Find nearby polygons with a point and search radius.
    Three lookup methods are supported:
        webmercator: radius (in km) is applied to search buffer in
            900913 (aka Google Spherical Mercator) projection.  This method
            is appropriate when used in conjuction with web maps.
        greatcircle: uses PostGIS ST_DWithin spatial query on a geography
            column, using great circle distances.
        point: simple test if point is inside polygons (e.g., radius=0)
    These methods assume the geometries are in a Geography column.  Edge
    cases across the dateline are handled correctly.
    Different methods are needed if a regular Geometry column is used
    in order to handle cases across the dateline."""
    region_list = ()
    default_method = 'webmercator'
    try:
        lon = float(request.GET['lon'])
        lat = float(request.GET['lat'])
        try:
            radius = float(request.GET['radius'])
        except:
            radius = 0.0 # km
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
        return render(request, 'spatialdata/regionlookup.json', {
            'region_list': region_list,
        }, content_type='application/json; charset=utf-8')
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
            point.transform(3857) # Proper Spherical Mercator srid
            point360.transform(3857)
            #mpa_list = Mpa.objects.filter(geom_smerc__dwithin=(point, Distance(km=radius))).defer(*Mpa.get_geom_fields())
            region_list = region.objects.filter(Q(geom_smerc__dwithin=(point, Distance(km=radius))) | Q(geom_smerc__dwithin=(point360, Distance(km=radius)))).defer(*region.get_geom_fields())
            search = point
        elif (method == 'webmercator_buffer'):
            point.transform(3857) # Proper Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000) # convert km to m, create buffer
            region_list = region.objects.filter(geog__intersects=searchbuffer).defer(*region.get_geom_fields())
            search = searchbuffer
        elif (method == 'webmercator_box'):
            point.transform(3857) # Proper Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000)
            region_list = region.objects.filter(geog__intersects=searchbuffer.envelope).defer(*region.get_geom_fields()) # use simple bounding box instead
            search = searchbuffer.envelope
        elif (method == 'webmercator_simple'):
            point.transform(3857) # Proper Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000, quadsegs=2) # simple buffer with 2 segs per quarter circle
            region_list = region.objects.filter(geog__intersects=searchbuffer).defer(*region.get_geom_fields())
            search = searchbuffer
        elif (method == 'greatcircle'):
            region_list = region.objects.filter(geog__dwithin=(point, Distance(km=radius))).defer(*region.get_geom_fields())
            search = point
        elif (method == 'point'):
            region_list = region.objects.filter(geog__intersects=point).defer(*region.get_geom_fields())
            search = point
        search.transform(4326)
        return render(request, 'spatialdata/regionlookup.json', {
            'search': search.coords,
            'region_list': region_list,
        }, content_type='application/json; charset=utf-8')

def nation_lookup_point_old(request, region):
    """Find nearby polygons with a point and search radius.
    Three lookup methods are supported:
        webmercator: radius (in km) is applied to search buffer in
            3857 (Spherical Mercator) projection.  This method
            is appropriate when used in conjuction with web maps.
        greatcircle: uses PostGIS ST_DWithin spatial query on a geography
            column, using great circle distances.
        point: simple test if point is inside polygons (e.g., radius=0)
    These methods assume the geometries are in a Geography column.  Edge
    cases across the dateline are handled correctly.
    Different methods are needed if a regular Geometry column is used
    in order to handle cases across the dateline."""
    region_list = ()
    default_method = 'webmercator'
    try:
        lon = float(request.GET['lon'])
        lat = float(request.GET['lat'])
        try:
            radius = float(request.GET['radius'])
        except:
            radius = 0.0 # km
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
        return render(request, 'spatialdata/regionlookup.json', {
            'region_list': region_list,
        }, content_type='application/json; charset=utf-8')
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
            point.transform(3857) # Spherical Mercator srid
            point360.transform(3857)
            #mpa_list = Mpa.objects.filter(geom_smerc__dwithin=(point, Distance(km=radius))).defer(*Mpa.get_geom_fields())
            region_list = region.objects.filter(Q(geom_smerc__dwithin=(point, Distance(km=radius))) | Q(geom_smerc__dwithin=(point360, Distance(km=radius)))).defer(*region.get_geom_fields())
            search = point
        elif (method == 'webmercator_buffer'):
            point.transform(3857) # Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000) # convert km to m, create buffer
            region_list = region.objects.filter(geog__intersects=searchbuffer).defer(*region.get_geom_fields())
            search = searchbuffer
        elif (method == 'webmercator_box'):
            point.transform(3857) # Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000)
            region_list = region.objects.filter(geog__intersects=searchbuffer.envelope).defer(*region.get_geom_fields()) # use simple bounding box instead
            search = searchbuffer.envelope
        elif (method == 'webmercator_simple'):
            point.transform(3857) # Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000, quadsegs=2) # simple buffer with 2 segs per quarter circle
            region_list = region.objects.filter(geog__intersects=searchbuffer).defer(*region.get_geom_fields())
            search = searchbuffer
        elif (method == 'greatcircle'):
            region_list = region.objects.filter(geog__dwithin=(point, Distance(km=radius))).defer(*region.get_geom_fields())
            search = point
        elif (method == 'point'):
            region_list = region.objects.filter(geog__intersects=point).defer(*region.get_geom_fields())
            search = point
        search.transform(4326)
        nation_list = Nation.objects.filter(pk__in=region_list.values_list('nation_id', flat=True).distinct())
        return render(request, 'spatialdata/regionlookup.json', {
            'search': search.coords,
            'region_list': nation_list,
        }, content_type='application/json; charset=utf-8')

