from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView
from mpa.models import Mpa
from mpa.views import mpas_norejects_nogeom, mpas_noproposed_nogeom, mpas_proposed_nogeom

class MapView(TemplateView):
    def get_context_data(self, **kwargs):
        mpas = mpas_norejects_nogeom.filter(is_mpa=True)
        context = super(MapView, self).get_context_data(**kwargs)
        context['mpa_count'] = {
            'implemented': mpas.filter(status__iexact='Designated', implemented=True).count(),
            'designated_unimplemented': mpas.filter(status__iexact='Designated', implemented=False).count(),
            'proposed': mpas.filter(status__iexact='Proposed').count(),
        }
        return context
