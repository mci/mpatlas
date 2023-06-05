from django.urls import path, re_path, include
from django.views.generic import TemplateView, DetailView, ListView

from wdpa.models import WdpaPoly_new

# from mpa.models import MpaCandidate
from wdpa.views import (
    WDPAListView,
    WDPAJsonListView,
    WDPAJsonView,
    get_wdpa_geom_json,
    lookup_point,
)

urlpatterns = [
    re_path(
        r"^sites/$",
        WDPAListView.as_view(
            queryset=WdpaPoly_new.objects.order_by("name").defer(
                *WdpaPoly_new.get_geom_fields()
            ),
            context_object_name="mpa_list",
            paginate_by=30,
            template_name="wdpa/WdpaPolygon_list.html",
        ),
        name="wdpa-siteslist",
    ),
    re_path(
        r"^sites/all/$",
        ListView.as_view(
            queryset=WdpaPoly_new.objects.order_by("name").defer(
                *WdpaPoly_new.get_geom_fields()
            ),
            context_object_name="mpa_list",
            # paginate_by=30,
            template_name="wdpa/WdpaPolygon_list.html",
        ),
        name="wdpa-siteslistall",
    ),
    re_path(
        r"^sites/json/$",
        WDPAJsonListView.as_view(
            queryset=WdpaPoly_new.objects.order_by("name").defer(
                *WdpaPoly_new.get_geom_fields()
            ),
            context_object_name="mpa_list",
            paginate_by=None,
            template_name="wdpa/WdpaPolygon_list.json",
        ),
        name="wdpa-siteslistjson",
    ),
    re_path(
        r"^sites/(?P<pk>\d+)/$",
        DetailView.as_view(
            model=WdpaPoly_new,
            queryset=WdpaPoly_new.objects.defer(*WdpaPoly_new.get_geom_fields()),
            context_object_name="mpa",
            template_name="wdpa/WdpaPolygon_detail.html",
        ),
        name="wdpa-siteinfo",
    ),
    re_path(
        r"^sites/(?P<pk>\d+)/json/$",
        WDPAJsonView.as_view(
            model=WdpaPoly_new,
            queryset=WdpaPoly_new.objects.all(),
            context_object_name="wdpa",
        ),
        name="wdpa-infojson",
    ),
    re_path(r"^sites/(?P<pk>\d+)/features/$", get_wdpa_geom_json, name="wdpa-geojson"),
    re_path(r"^lookup/point/$", lookup_point),
]
