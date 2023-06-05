from django.urls import path, re_path, include
from django.views.generic import TemplateView, DetailView, ListView
from campaign.views import JsonListView, get_campaign_pointgeom_json, edit_campaign_geom

from campaign.models import Campaign, Initiative

urlpatterns = [
    # Examples:
    # re_path(r'^$', 'mpatlas.views.home', name='home'),
    # re_path(r'^mpatlas/', include('mpatlas.foo.urls')),
    # re_path(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    # re_path(r'^sites/', 'wdpa.views.sitelist'),
    # re_path(r'^sites/(?P<siteid>\d)/$', 'wdpa.views.siteinfo'),
    # re_path(r'^map/$', 'campaign.views.map'),
    re_path(
        r"^$",
        ListView.as_view(
            queryset=Campaign.objects.all().order_by("name"),
            context_object_name="campaign_list",
            paginate_by=None,
            template_name="campaign/Campaign_map.html",
        ),
        name="campaign-map",
    ),
    re_path(
        r"^list/$",
        ListView.as_view(
            queryset=Campaign.objects.all().order_by("name"),
            context_object_name="campaign_list",
            paginate_by=60,
            template_name="campaign/Campaign_list.html",
        ),
        name="campaign-list",
    ),
    re_path(
        r"list/geojson/$",
        JsonListView.as_view(
            queryset=Campaign.objects.filter(point_geom__isnull=False).order_by("name"),
            context_object_name="campaign_list",
            paginate_by=None,
            template_name="campaign/Campaign_list_geojson.json",
        ),
        name="campaign-list-geojson",
    ),
    re_path(
        r"^(?P<pk>\d+)/$",
        DetailView.as_view(
            model=Campaign,
            queryset=Campaign.objects.all().order_by("name"),
            context_object_name="campaign",
            template_name="campaign/Campaign_detail.html",
        ),
        name="campaign-info-byid",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/$",
        DetailView.as_view(
            model=Campaign,
            queryset=Campaign.objects.all().order_by("name"),
            context_object_name="campaign",
            template_name="campaign/Campaign_detail.html",
        ),
        name="campaign-info",
    ),
    re_path(
        r"^(?P<pk>\d+)/point/$",
        get_campaign_pointgeom_json,
        name="campaign-point-geojson",
    ),
    re_path(
        r"^(?P<pk_or_slug>[\d\w-]+)/edit/geo/$",
        edit_campaign_geom,
        name="campaign-editgeom",
    ),
    re_path(
        r"^initiative/(?P<pk>\d+)/$",
        DetailView.as_view(
            model=Initiative,
            queryset=Initiative.objects.all().order_by("name"),
            context_object_name="initiative",
            template_name="campaign/Initiative_detail.html",
        ),
        name="initiative-info-byid",
    ),
    re_path(
        r"^initiative/(?P<slug>[\w-]+)/$",
        DetailView.as_view(
            model=Initiative,
            queryset=Initiative.objects.all().order_by("name"),
            context_object_name="initiative",
            template_name="campaign/Initiative_detail.html",
        ),
        name="initiative-info",
    ),
    # re_path(r'^(?P<pk>\d+)/edit/$', 'campaign.views.edit_campaign', name='campaign-edit'),
    # re_path(r'^lookup/point/$', 'mpa.views.lookup_point'),
]
