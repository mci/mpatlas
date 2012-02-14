from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView, DetailView, ListView

from spatialdata.models import Eez
from spatialdata.views import EezListView, EezJsonListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    
    url(r'^eez/$',
        EezListView.as_view(
            queryset=Eez.objects.order_by('eez').defer(*Eez.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='eez-list'),
    url(r'^eez/json/$',
        EezJsonListView.as_view(
            queryset=Eez.objects.order_by('name').defer(*Eez.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=None,
            template_name='mpa/Mpa_list.json'),
        name='eez-listjson'),
    url(r'^eez/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Eez,
            queryset=Eez.objects.defer(*Eez.get_geom_fields()),
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.html'),
        name='eez-info'),
    url(r'^eez/(?P<pk>\d+)/json/$',
        DetailView.as_view(
            model=Eez,
            queryset=Eez.objects.defer(*Eez.get_geom_fields()),
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.json'),
        name='eez-infojson'),
    url(r'^eez/(?P<pk>\d+)/features/$', 'spatialdata.views.get_eez_geom_json', name='eez-geojson'),

    url(r'^eez/lookup/point/$', 'spatialdata.views.region_lookup_point', {'region': Eez}),
)
