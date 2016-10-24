from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import ListView

from django.contrib.gis import geos, gdal
from django.contrib.gis.measure import Distance

# import reversion
from reversion import revisions as reversion
from reversion.models import Revision
from django.db import connection, transaction

from campaign.models import Campaign

def get_campaign_pointgeom_json(request, pk, simplified=True, webmercator=False):
    geomfield = 'point_geom'
    campaign = Campaign.objects.geojson(field_name=geomfield).get(pk=pk)
    return HttpResponse(campaign.geojson, content_type='application/json; charset=utf-8')

class JsonListView(ListView):
    def render_to_response(self, context, **kwargs):
        return super(JsonListView, self).render_to_response(context, content_type='application/json; charset=utf-8', **kwargs)

