from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView, DetailView, ListView

from mpa.models import Mpa, MpaCandidate
from mpa.views import MpaListView, MpaJsonListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    
    #url(r'^sites/', 'wdpa.views.sitelist'),
    #url(r'^sites/(?P<siteid>\d)/$', 'wdpa.views.siteinfo'),
    
    url(r'^sites/$',
        MpaListView.as_view(
            queryset=Mpa.objects.order_by('name').defer(*Mpa.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='mpa/MpaPolygon_list.html'),
        name='mpa-siteslist'),
    url(r'^sites/all/$',
        ListView.as_view(
            queryset=Mpa.objects.order_by('name').defer(*Mpa.get_geom_fields()),
            context_object_name='mpa_list',
            #paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='mpa-siteslistall'),
    url(r'^sites/json/$',
        MpaJsonListView.as_view(
            queryset=Mpa.objects.order_by('name').defer(*Mpa.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=None,
            template_name='mpa/Mpa_list.json'),
        name='mpa-siteslistjson'),
    url(r'^sites/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Mpa,
            queryset=Mpa.objects.defer(*Mpa.get_geom_fields()),
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.html'),
        name='mpa-siteinfo'),
    
    url(r'^lookup/point/$', 'mpa.views.lookup_point'),
    
    url(r'^proposed/$',
        MpaListView.as_view(
            queryset=MpaCandidate.objects.order_by('name').defer(*MpaCandidate.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='mpa-candidate-siteslist'),
    url(r'^proposed/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=MpaCandidate,
            queryset=MpaCandidate.objects.defer(*MpaCandidate.get_geom_fields()),
            context_object_name='mpa',
            template_name='mpa/MpaCandidate_detail.html'),
        name='mpa-candidate-siteinfo'),
)

