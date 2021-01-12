from django.conf.urls import include, url
from django.views.generic import TemplateView, DetailView, ListView, RedirectView

from spatialdata.models import Nation, Eez, Meow
from spatialdata.views import nations_nogeom, EezListView, EezJsonListView, get_country_geom_json, region_lookup_point, get_geom_json

urlpatterns = [
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    
    url(r'^nation/(?P<extrapath>.*)$', RedirectView.as_view(
        url='/region/country/%(extrapath)s',
        permanent=False,
        query_string=True
    )),
    url(r'^country/$',
        EezListView.as_view(
            queryset=nations_nogeom.order_by('name'),
            context_object_name='country_list',
            paginate_by=None,
            template_name='spatialdata/Country_list.html'),
        name='country-list'),
    url(r'^country/json/$',
        EezJsonListView.as_view(
            queryset=nations_nogeom.order_by('name'),
            context_object_name='country_list',
            paginate_by=None,
            template_name='spatialdata/Country_list.json'),
        name='country-listjson'),
    url(r'^country/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Nation,
            queryset=nations_nogeom,
            context_object_name='country',
            template_name='spatialdata/Country_detail.html'),
        name='country-info-pk'),
    url(r'^country/(?P<iso3code>\w+)/$',
        DetailView.as_view(
            model=Nation,
            queryset=nations_nogeom,
            slug_field='iso3code',
            slug_url_kwarg='iso3code',
            context_object_name='country',
            template_name='spatialdata/Country_detail.html'),
        name='country-info'),
    url(r'^country/(?P<iso3code>\w+)/json/$',
        DetailView.as_view(
            model=Nation,
            queryset=nations_nogeom,
            slug_field='iso3code',
            slug_url_kwarg='iso3code',
            context_object_name='country',
            template_name='spatialdata/Country_detail.json'),
        name='country-infojson'),
    url(r'^country/(?P<iso3code>\w+)/features/$', get_country_geom_json, name='country-geojson'),

    # url(r'^country/lookup/point/$', country_lookup_point, {'region': Eez}),
    url(r'^country/lookup/point/$', region_lookup_point, {'region': Nation}),
    
    
    url(r'^eez/$',
        EezListView.as_view(
            queryset=Eez.objects.order_by('eez').defer(*Eez.get_geom_fields()),
            context_object_name='country_list',
            paginate_by=30,
            template_name='spatialdata/Country_list.html'),
        name='eez-list'),
    url(r'^eez/json/$',
        EezJsonListView.as_view(
            queryset=Eez.objects.order_by('eez').defer(*Eez.get_geom_fields()),
            context_object_name='country_list',
            paginate_by=None,
            template_name='spatialdata/Country_list.json'),
        name='eez-listjson'),
    url(r'^eez/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Eez,
            queryset=Eez.objects.defer(*Eez.get_geom_fields()),
            context_object_name='country',
            template_name='spatialdata/Country_detail.html'),
        name='eez-info'),
    url(r'^eez/(?P<pk>\d+)/json/$',
        DetailView.as_view(
            model=Eez,
            queryset=Eez.objects.defer(*Eez.get_geom_fields()),
            context_object_name='mpa',
            template_name='spatialdata/Country_detail.json'),
        name='eez-infojson'),
    url(r'^eez/(?P<pk>\d+)/features/$', get_geom_json, {'model': Eez}, name='eez-geojson'),

    url(r'^eez/lookup/point/$', region_lookup_point, {'region': Eez}),
    
    
    url(r'^meow/$',
        EezListView.as_view(
            queryset=Meow.objects.order_by('ecoregion').defer(*Meow.get_geom_fields()),
            context_object_name='country_list',
            paginate_by=30,
            template_name='spatialdata/Country_list.html'),
        name='meow-list'),
    url(r'^meow/json/$',
        EezJsonListView.as_view(
            queryset=Meow.objects.order_by('ecoregion').defer(*Meow.get_geom_fields()),
            context_object_name='country_list',
            paginate_by=None,
            template_name='spatialdata/Country_list.json'),
        name='meow-listjson'),
    url(r'^meow/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Meow,
            queryset=Meow.objects.defer(*Meow.get_geom_fields()),
            context_object_name='country',
            template_name='spatialdata/Country_detail.html'),
        name='meow-info'),
    url(r'^meow/(?P<pk>\d+)/json/$',
        DetailView.as_view(
            model=Meow,
            queryset=Eez.objects.defer(*Meow.get_geom_fields()),
            context_object_name='country',
            template_name='spatialdata/Country_detail.json'),
        name='eez-infojson'),
    url(r'^meow/(?P<pk>\d+)/features/$', get_geom_json, {'model': Meow}, name='meow-geojson'),
    
    url(r'^meow/lookup/point/$', region_lookup_point, {'region': Meow}),
]
