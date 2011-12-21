from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView, DetailView, ListView

from wdpa.models import WdpaPolygon
from wdpa.views import MpaListView, MpaJsonListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    
    #url(r'^sites/', 'wdpa.views.sitelist'),
    #url(r'^sites/(?P<siteid>\d)/$', 'wdpa.views.siteinfo'),
    
    url(r'^sites/$',
        ListView.as_view(
            queryset=WdpaPolygon.objects.order_by('name').defer(*WdpaPolygon.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='wdpa/WdpaPolygon_list.html'),
        name='wdpa-siteslist'),
    url(r'^sites/all/$',
        ListView.as_view(
            queryset=WdpaPolygon.objects.order_by('name').defer(*WdpaPolygon.get_geom_fields()),
            context_object_name='mpa_list',
            #paginate_by=30,
            template_name='wdpa/WdpaPolygon_list.html'),
        name='wdpa-siteslistall'),
    url(r'^sites/json/$',
        MpaJsonListView.as_view(
            queryset=WdpaPolygon.objects.order_by('name').defer(*WdpaPolygon.get_geom_fields()),
            context_object_name='mpa_list',
            paginate_by=None,
            template_name='wdpa/WdpaPolygon_list.json'),
        name='wdpa-siteslistall'),
    url(r'^sites/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=WdpaPolygon,
            queryset=WdpaPolygon.objects.defer('geog', 'geom', 'geom_smerc'),
            context_object_name='mpa',
            template_name='wdpa/WdpaPolygon_detail.html'),
        name='wdpa-siteinfo'),
    url(r'^lookup/point/$', 'wdpa.views.lookup_point'),
)
