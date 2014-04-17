from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, DetailView, ListView
from campaign.views import JsonListView

from campaign.models import Campaign, Initiative

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    
    #url(r'^sites/', 'wdpa.views.sitelist'),
    #url(r'^sites/(?P<siteid>\d)/$', 'wdpa.views.siteinfo'),
    
    # url(r'^map/$', 'campaign.views.map'),

    url(r'^$',
        TemplateView.as_view(template_name='campaign/Campaign_map.html'),
        name='campaign-map'),
    url(r'^list/$',
        ListView.as_view(
            queryset=Campaign.objects.all().order_by('name'),
            context_object_name='campaign_list',
            paginate_by=60,
            template_name='campaign/Campaign_list.html'),
        name='campaign-list'),
    url(r'list/geojson/$',
        JsonListView.as_view(
            queryset=Campaign.objects.filter(point_geom__isnull=False).order_by('name'),
            context_object_name='campaign_list',
            paginate_by=None,
            template_name='campaign/Campaign_list_geojson.json'),
        name='campaign-list-geojson'),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Campaign,
            queryset=Campaign.objects.all().order_by('name'),
            context_object_name='campaign',
            template_name='campaign/Campaign_detail.html'),
        name='campaign-info-byid'),
    url(r'^(?P<slug>[\w-]+)/$',
        DetailView.as_view(
            model=Campaign,
            queryset=Campaign.objects.all().order_by('name'),
            context_object_name='campaign',
            template_name='campaign/Campaign_detail.html'),
        name='campaign-info'),
    url(r'^(?P<pk>\d+)/point/$', 'campaign.views.get_campaign_pointgeom_json', name='campaign-point-geojson'),
    
    url(r'^initiative/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Initiative,
            queryset=Initiative.objects.all().order_by('name'),
            context_object_name='initiative',
            template_name='campaign/Initiative_detail.html'),
        name='initiative-info-byid'),
    url(r'^initiative/(?P<slug>[\w-]+)/$',
        DetailView.as_view(
            model=Initiative,
            queryset=Initiative.objects.all().order_by('name'),
            context_object_name='initiative',
            template_name='campaign/Initiative_detail.html'),
        name='initiative-info'),

    # url(r'^(?P<pk>\d+)/edit/$', 'campaign.views.edit_campaign', name='campaign-edit'),
    
    # url(r'^lookup/point/$', 'mpa.views.lookup_point'),
)

