from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import ListView
from django.db.models import Q
import re
from itertools import chain
import json

from django.contrib.gis import geos, gdal
from django.contrib.gis.measure import Distance

from mpa.models import Mpa, MpaCandidate, mpas_all_nogeom, mpas_noproposed_nogeom, mpas_proposed_nogeom
from mpa.forms import MpaForm, MpaGeomForm

from mpa.filters import apply_filters

import reversion
from django.db import connection, transaction
from reversion.models import Revision
from mpa.models import Mpa, Contact, WikiArticle, VersionMetadata

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

def do_revision(request):
    mpa = Mpa.objects.get(pk=4)
    mpa.summary = 'Test123'
    mpa.save()
    reversion.set_comment('Test comment')

@never_cache
@transaction.commit_on_success
@reversion.create_revision()
def revision_view(request):
    do_revision(request)
    mpa = Mpa.objects.get(pk=4)
    versions = len(reversion.get_for_object(mpa))
    return HttpResponse('Attempted to save a revision - %s' % (versions))

@never_cache
@transaction.commit_on_success
@reversion.create_revision()
def revision_view2(request):
    rcm = reversion.revision_context_manager
    rc = rcm.create_revision()
    rcm.start(manage_manually=False)
    #rcm.start(manage_manually=True)
    print rcm.is_active(), rcm.is_invalid(), rcm.is_managing_manually()
    mpa = Mpa.objects.get(pk=4)
    mpa.summary = 'Test2'
    mpa.save()
    rcm.set_comment('Test comment')
    rcm.end()
    return HttpResponse('Attempted to save a revision - 2')

@login_required
@transaction.commit_on_success
@reversion.create_revision()
def edit_mpa(request, pk):
    mpa = get_object_or_404(Mpa, pk=pk)
    if (request.POST):
        # Got a form submission
        editform = MpaForm(request.POST, instance=mpa)
        if editform.is_valid():
            mpasaved = editform.save()
            try:
                reversion.set_comment(editform.cleaned_data.get("edit_comment"))
            except:
                pass
            try:
                reversion.set_user(request.user)
            except:
                pass
            try:
                reversion.add_meta(VersionMetadata, comment=editform.cleaned_data.get("edit_comment"), reference=editform.cleaned_data.get("edit_reference"))
            except:
                pass
            return HttpResponseRedirect(reverse('mpa-siteinfo', kwargs={'pk': pk}))
    else:
        editform = MpaForm(instance=mpa)
    return render_to_response('mpa/Mpa_editform.html', {
        'form': editform,
        'mpa': mpa,
        'respond_url': reverse('mpa-editsite', kwargs={'pk': pk}),
    }, context_instance=RequestContext(request))

@login_required
@transaction.commit_on_success
@reversion.create_revision()
def edit_mpa_geom(request, pk):
    mpa = get_object_or_404(Mpa, pk=pk)
    if (request.POST):
        # Got a form submission
        editform = MpaGeomForm(request.POST, request.FILES, instance=mpa)
        if editform.is_valid():
            try:
                if 'boundaryfile' in request.FILES:
                    # Use uploaded file 'boundaryfile' instead of textarea 'boundarygeo'
                    gj = json.load(request.FILES['boundaryfile'])
                else:
                    # Use 'boundarygeo' textarea
                    gj = editform.cleaned_data['boundarygeo']
                if 'type' in gj and gj['type'] == 'FeatureCollection':
                    # Use first feature in collection and ignore the rest
                    geom_geojson = gj['features'][0]['geometry']
                elif 'type' in gj and gj['type'] == 'Feature':
                    geom_geojson = gj['geometry']
                else:
                    geom_geojson = gj
                geom_geojson = json.dumps(geom_geojson) 
                if (geom_geojson) == '':
                    mpa.geom = None
                    mpa.point_geom = None
                else:
                    geom = geos.GEOSGeometry(geom_geojson)
                    if geom.geom_type in ('Point', 'MultiPoint'):
                        if geom.geom_type == 'Point':
                            geom = geos.MultiPoint(geom)
                        mpa.point_geom = geom
                    elif geom.geom_type in ('Polygon', 'MultiPolygon'):
                        if geom.geom_type == 'Polygon':
                            geom = geos.MultiPolygon(geom)
                        mpa.geom = geom
            except:
                raise
            mpa.save()
            # mpasaved = editform.save()
            # mpasaved.set_geog_from_geom()
            # mpasaved.make_simplified_geom()
            try:
                reversion.set_comment("Boundary geometry updated.")
            except:
                pass
            try:
                reversion.set_user(request.user)
            except:
                pass
            return HttpResponseRedirect(reverse('mpa-siteinfo', kwargs={'pk': pk}))
    else:
        initialdata = {}
        if mpa.geom:
            initialdata['boundarygeo'] = mpa.geom.geojson
        editform = MpaGeomForm(initial=initialdata)
    return render_to_response('mpa/Mpa_editgeoform.html', {
        'form': editform,
        'mpa': mpa,
        'respond_url': reverse('mpa-editsitegeom', kwargs={'pk': pk}),
    }, context_instance=RequestContext(request))


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
        qs = self.queryset
        try:
            q = self.request.GET.get('q')
            if q:
                #return self.queryset.filter(name__istartswith=q)
                # \m is Postgresql regex word boundary, Python used \b
                # (?i) is a Postgresql regex mode modifier to make regex case insensitive
                qs = qs.filter(name__regex=ur'(?i)\m' + re.sub(r'([.*/\|^$:(){}\'"+&?])', r'\\\1', q))
            sortby = self.request.GET.get('sort')
            direction = self.request.GET.get('dir')
            if sortby:
                dirflag = '-' if (direction and direction.lower() == 'desc') else ''
                qs = qs.order_by(dirflag + sortby)
            # Apply specified filters
            filters = self.request.GET.get('filter')
            if filters:
                qs = apply_filters(qs, filters)
            return qs
        except:
            pass
        else:
            return self.queryset

class MpaJsonListView(MpaListView):
    def render_to_response(self, context, **kwargs):
        return super(MpaJsonListView, self).render_to_response(context, content_type='application/json; charset=utf-8', **kwargs)

def get_mpa_geom_wkt(request, pk, simplified=True, webmercator=False):
    geomfield = 'geom'
    if (webmercator):
        geomfield = 'geom_smerc'
    if simplified:
        geomfield = 'simple_' + geomfield
    mpa = Mpa.objects.only(geomfield).get(pk=pk)
    return HttpResponse(getattr(mpa,geomfield).wkt, content_type='text/plain; charset=utf-8')

def get_mpa_geom_json(request, pk, simplified=True, webmercator=False):
    try:
        simplified = request.GET['simplified'].lower() not in ('false', 'f', 'no', '0', 0)
    except:
        pass
    try:
        webmercator = (request.GET['webmercator'].upper() == 'TRUE')
    except:
        pass
    geomfield = sgeomfield = 'geom'
    if (webmercator):
        geomfield = 'geom_smerc'
    mpaq = Mpa.objects.geojson(field_name=geomfield).geojson(field_name='point_within', model_att='geojson_point').defer(*Mpa.get_geom_fields())
    if simplified:
        sgeomfield = 'simple_' + geomfield
        mpaq = mpaq.geojson(field_name=sgeomfield, model_att='geojson_simple')
    mpa = mpaq.get(pk=pk)
    if mpa.is_point:
        geojson = mpa.geojson_point
    else:
        geojson = mpa.geojson if not simplified else mpa.geojson_simple
    if not geojson and simplified:
        geojson = mpa.geojson
    return HttpResponse(geojson or '{}', content_type='application/json; charset=utf-8')


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
        return render(request, 'mpa/mpalookup.json', {
            'mpa_list': mpa_list,
        }, content_type='application/json; charset=utf-8')
    else:
        mpas_valid = mpas_noproposed_nogeom
        # We need to normalize the longitude into the range -180 to 180 so we don't
        # make the cast to PostGIS Geography type complain
        point = geos.Point(normalize_lon(lon), lat, srid=gdal.SpatialReference('WGS84').srid) # srid=4326 , WGS84 geographic
        origpoint = point.clone()
        if (method == 'webmercator'):
            if (normalize_lon(lon) < 0):
                lon360 = normalize_lon(lon) + 360
            else:
                lon360 = normalize_lon(lon) - 360
            point360 = geos.Point(lon360, lat, srid=gdal.SpatialReference('WGS84').srid)
            point.transform(3857) # Google Spherical Mercator srid
            point360.transform(3857)
            #mpa_list = Mpa.objects.filter(geom_smerc__dwithin=(point, Distance(km=radius))).defer(*Mpa.get_geom_fields())
            mpa_list = mpas_valid.filter(Q(geom_smerc__dwithin=(point, Distance(km=radius))) | Q(geom_smerc__dwithin=(point360, Distance(km=radius)))).defer(*Mpa.get_geom_fields())
            search = point
        elif (method == 'webmercator_buffer'):
            point.transform(3857) # Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000) # convert km to m, create buffer
            mpa_list = mpas_valid.filter(geog__intersects=searchbuffer).defer(*Mpa.get_geom_fields())
            search = searchbuffer
        elif (method == 'webmercator_box'):
            point.transform(3857) # Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000)
            mpa_list = mpas_valid.filter(geog__intersects=searchbuffer.envelope).defer(*Mpa.get_geom_fields()) # use simple bounding box instead
            search = searchbuffer.envelope
        elif (method == 'webmercator_simple'):
            point.transform(3857) # Spherical Mercator srid
            searchbuffer = point.buffer(radius * 1000, quadsegs=2) # simple buffer with 2 segs per quarter circle
            mpa_list = mpas_valid.filter(geog__intersects=searchbuffer).defer(*Mpa.get_geom_fields())
            search = searchbuffer
        elif (method == 'greatcircle'):
            mpa_list = mpas_valid.filter(geog__dwithin=(point, Distance(km=radius))).defer(*Mpa.get_geom_fields())
            search = point
        elif (method == 'point'):
            mpa_list = mpas_valid.filter(geog__intersects=point).defer(*Mpa.get_geom_fields())
            search = point
        candidate_radius = radius * 2.2 # We're using big icons on a point, this let's us catch it better
        mpa_candidate_list = mpas_proposed_nogeom.filter(point_geog__dwithin=(origpoint, Distance(km=candidate_radius)))
        #mpa_candidate_list = mpas_proposed_nogeom
        # mpa_list = list(mpa_list)
        # ids = [m.mpa_id for m in mpa_list]
        # cleaned_mpa_list
        # for mpa in mpa_list:
        #     if mpa.mpa_id >= 7700000:
        #         orig_id = int(str(mpa_id)[-5:])
        #         if orig_id in ids:
        #             ids.remove(orig_id)
        # for mpa in mpa_list:
        #     if mpa.mpa_id in ids:
        #         cleaned_mpa_list.append(mpa)
        search.transform(4326)
        return render(request, 'mpa/mpalookup.json', {
            'search': search.coords,
            'mpa_list': mpa_list,
            'mpa_candidate_list': mpa_candidate_list,
        }, content_type='application/json; charset=utf-8')
