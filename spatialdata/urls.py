from django.conf.urls import include, url
from django.views.generic import TemplateView, DetailView, ListView

from spatialdata.models import Nation, Eez, Meow
from spatialdata.views import EezListView, EezJsonListView, get_nation_geom_json, region_lookup_point, get_geom_json

urlpatterns = [
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    
    url(r'^nation/$',
        EezListView.as_view(
            queryset=Nation.objects.all().order_by('name'),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='nation-list'),
    url(r'^nation/json/$',
        EezJsonListView.as_view(
            queryset=Nation.objects.all().order_by('name'),
            context_object_name='mpa_list',
            paginate_by=None,
            template_name='mpa/Mpa_list.json'),
        name='nation-listjson'),
    url(r'^nation/(?P<iso3code>\w+)/$',
        DetailView.as_view(
            model=Nation,
            queryset=Nation.objects.all(),
            slug_field='iso3code',
            slug_url_kwarg='iso3code',
            context_object_name='nation',
            template_name='spatialdata/Nation_detail.html'),
        name='nation-info'),
    url(r'^nation/(?P<iso3code>\w+)/json/$',
        DetailView.as_view(
            model=Nation,
            queryset=Nation.objects.all(),
            slug_field='iso3code',
            slug_url_kwarg='iso3code',
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.json'),
        name='nation-infojson'),
    url(r'^nation/(?P<iso3code>\w+)/features/$', get_nation_geom_json, name='nation-geojson'),

    # url(r'^nation/lookup/point/$', nation_lookup_point, {'region': Eez}),
    url(r'^nation/lookup/point/$', region_lookup_point, {'region': Nation}),
    
    
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
    url(r'^eez/(?P<pk>\d+)/features/$', get_geom_json, {'model': Eez}, name='eez-geojson'),

    url(r'^eez/lookup/point/$', region_lookup_point, {'region': Eez}),
    
    
    url(r'^meow/$',
        EezListView.as_view(
            queryset=Meow.objects.order_by('name').defer(*Meow.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='meow-list'),
    url(r'^meow/json/$',
        EezJsonListView.as_view(
            queryset=Meow.objects.order_by('name').defer(*Meow.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=None,
            template_name='mpa/Mpa_list.json'),
        name='meow-listjson'),
    url(r'^meow/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Meow,
            queryset=Meow.objects.defer(*Meow.get_geom_fields()),
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.html'),
        name='meow-info'),
    url(r'^meow/(?P<pk>\d+)/json/$',
        DetailView.as_view(
            model=Meow,
            queryset=Eez.objects.defer(*Meow.get_geom_fields()),
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.json'),
        name='eez-infojson'),
    url(r'^meow/(?P<pk>\d+)/features/$', get_geom_json, {'model': Meow}, name='meow-geojson'),
    
    url(r'^meow/lookup/point/$', region_lookup_point, {'region': Meow}),
]
