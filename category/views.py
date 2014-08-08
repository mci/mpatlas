from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from category.models import Category, Details, TaggedItem
from mpa.models import Mpa, mpas_norejects_nogeom
from campaign.models import Campaign

class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(**kwargs)
		context['member_mpas'] = mpas_norejects_nogeom.filter(categories__slug=self.object.slug)
		context['member_campaigns'] = Campaign.objects.filter(categories__slug=self.object.slug)
		return context
