from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView

from django.contrib.contenttypes.models import ContentType

from category.models import Category, Details, TaggedItem
from mpa.models import Mpa
from mpa.views import mpas_norejects_nogeom
from campaign.models import Campaign

class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        mpa_type = ContentType.objects.get_for_model(Mpa)
        mpa_ids = TaggedItem.objects.filter(tag=self.object,content_type=mpa_type).values_list('object_id', flat=True)
        context['member_mpas'] = mpas_norejects_nogeom.filter(pk__in=mpa_ids).order_by('country','name')
        # context['member_mpas'] = mpas_norejects_nogeom.filter(categories__slug=self.object.slug)
        context['member_campaigns'] = Campaign.objects.filter(categories__slug=self.object.slug)
        return context

class CategoryGeoJsonView(DetailView):
    template_name = "category/Category_geojson.json"
    content_type = 'application/json; charset=utf-8'

    def get_context_data(self, **kwargs):
        context = super(CategoryGeoJsonView, self).get_context_data(**kwargs)
        mpa_type = ContentType.objects.get_for_model(Mpa)
        mpa_ids = TaggedItem.objects.filter(tag=self.object,content_type=mpa_type).values_list('object_id', flat=True)
        context['member_mpas'] = mpas_norejects_nogeom.filter(pk__in=mpa_ids).only('name', 'summary', 'is_point', 'point_geom').geojson(field_name='simple_geom', precision=6).order_by('country','name')
        # context['member_mpas'] = mpas_norejects_nogeom.filter(categories__slug=self.object.slug)
        context['member_campaigns'] = Campaign.objects.filter(categories__slug=self.object.slug).only('name', 'summary').geojson(field_name='point_geom')
        return context