from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import RequestContext
from django.views.generic import ListView

from django.contrib.gis import geos, gdal
from django.contrib.gis.measure import Distance

# import reversion
from reversion import revisions as reversion
from reversion.models import Revision
from django.db import connection, transaction
from django.contrib.gis import geos, gdal
from django.contrib.auth.decorators import login_required
import json

from campaign.models import Campaign
from campaign.forms import CampaignGeomForm

def get_campaign_pointgeom_json(request, pk, simplified=True, webmercator=False):
    geomfield = 'point_geom'
    campaign = Campaign.objects.geojson(field_name=geomfield).get(pk=pk)
    return HttpResponse(campaign.geojson, content_type='application/json; charset=utf-8')

class JsonListView(ListView):
    def render_to_response(self, context, **kwargs):
        return super(JsonListView, self).render_to_response(context, content_type='application/json; charset=utf-8', **kwargs)

@login_required
@transaction.atomic
@reversion.create_revision()
def edit_campaign_geom(request, pk_or_slug):
    queryset = Campaign.objects.all()
    # Next, try looking up by primary key.
    if pk_or_slug is not None:   
        try:
            queryset_pk = queryset.filter(pk=pk_or_slug)
            # Get the single item from the filtered queryset
            obj = queryset_pk.get()
        except:
            try:
                # Next, try looking up by slug.
                slug_field = 'slug'
                queryset_slug = queryset.filter(**{slug_field: pk_or_slug})
                obj = queryset_slug.get()
            except queryset.model.DoesNotExist:
                raise Http404(_("No %(verbose_name)s found matching the query via pk or slug") %
                              {'verbose_name': queryset.model._meta.verbose_name})
    else:
        raise AttributeError(
            "View must be called with either an object pk or a slug in the URLconf."
        )

    campaign = obj
    # campaign = get_object_or_404(Campaign, pk=pk)
    
    if (request.POST):
        # Got a form submission
        editform = CampaignGeomForm(request.POST, request.FILES, instance=campaign)
        if editform.is_valid():
            try:
                if 'boundaryfile' in request.FILES:
                    # Use uploaded file 'boundaryfile' instead of textarea 'boundarygeo'
                    gj = json.load(request.FILES['boundaryfile'])
                else:
                    # Use 'boundarygeo' textarea
                    gj = json.loads(editform.cleaned_data['boundarygeo'])
                if 'type' in gj and gj['type'] == 'FeatureCollection':
                    # Use first feature in collection and ignore the rest
                    geom_geojson = gj['features'][0]['geometry']
                elif 'type' in gj and gj['type'] == 'Feature':
                    geom_geojson = gj['geometry']
                else:
                    geom_geojson = gj
                geom_geojson = json.dumps(geom_geojson) 
                if (geom_geojson) == '':
                    campaign.geom = None
                    campaign.point_geom = None
                else:
                    geom = gdal.OGRGeometry(geos.GEOSGeometry(geom_geojson).ewkb)
                    geom.coord_dim = 2  # Force 2D, drop all z coords
                    geom = geom.geos
                    if geom.geom_type in ('Point', 'MultiPoint'):
                        # if geom.geom_type == 'Point':
                        #     geom = geos.MultiPoint(geom)
                        if geom.geom_type == 'MultiPoint':
                            geom = geom[0] # just take first point
                        campaign.point_geom = geom
                        campaign.geom = None
                        campaign.is_point = True
                    elif geom.geom_type in ('Polygon', 'MultiPolygon'):
                        if geom.geom_type == 'Polygon':
                            geom = geos.MultiPolygon(geom)
                        campaign.geom = geom
                        campaign.point_geom = None
                        campaign.is_point = False
            except:
                raise
            campaign.save()
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
            return HttpResponseRedirect(reverse('campaign-info', kwargs={'slug': campaign.slug}))
    else:
        initialdata = {}
        if campaign.geom:
            initialdata['boundarygeo'] = campaign.geom.geojson
        elif campaign.point_geom:
            initialdata['boundarygeo'] = campaign.point_geom.geojson
        editform = CampaignGeomForm(initial=initialdata)
    return render(request, 'campaign/Campaign_editgeoform.html', {
        'form': editform,
        'campaign': campaign,
        'respond_url': reverse('campaign-editgeom', kwargs={'pk_or_slug': pk_or_slug}),
    })