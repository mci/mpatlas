from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from django.contrib.contenttypes.models import ContentType

from category.models import Category, Details, TaggedItem
from mpa.models import Mpa, mpas_norejects_nogeom
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