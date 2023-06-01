from django.conf.urls import include, url
from django.views.generic import TemplateView, DetailView, ListView

from wdpa.models import WdpaPoly_new

# from mpa.models import MpaCandidate
from wdpa.views import WDPAListView, WDPAJsonListView, lookup_point

urlpatterns = [
    url(
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
    url(
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
    url(
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
    url(
        r"^sites/(?P<pk>\d+)/$",
        DetailView.as_view(
            model=WdpaPoly_new,
            queryset=WdpaPoly_new.objects.defer(*WdpaPoly_new.get_geom_fields()),
            context_object_name="mpa",
            template_name="wdpa/WdpaPolygon_detail.html",
        ),
        name="wdpa-siteinfo",
    ),
    url(r"^lookup/point/$", lookup_point),
]
