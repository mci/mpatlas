from django.urls import path, re_path, include
from django.views.generic import TemplateView, DetailView, ListView

from mpa.models import Mpa, MpaCandidate
from mpa.views import (
    MpaListView,
    MpaJsonListView,
    MpaJsonView,
    get_mpa_geom_json,
    edit_mpa,
    edit_mpa_geom,
    lookup_point,
)
from mpa.views import revision_view, revision_view2
from mpa.views import (
    mpas_all_nogeom,
    mpas_norejects_nogeom,
    mpas_noproposed_nogeom,
    mpas_proposed_nogeom,
)

urlpatterns = [
    # Examples:
    # re_path(r'^$', 'mpatlas.views.home', name='home'),
    # re_path(r'^mpatlas/', include('mpatlas.foo.urls')),
    # re_path(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    # re_path(r'^sites/', 'wdpa.views.sitelist'),
    # re_path(r'^sites/(?P<siteid>\d)/$', 'wdpa.views.siteinfo'),
    re_path(r"^revision/$", revision_view),
    re_path(r"^revision2/$", revision_view2),
    re_path(
        r"^sites/$",
        MpaListView.as_view(
            queryset=mpas_norejects_nogeom.order_by("name").only(
                "name",
                "designation_eng",
                "country",
                "mpa_id",
                "status",
                "point_within",
                "bbox_lowerleft",
                "bbox_upperright",
            ),
            context_object_name="mpa_list",
            paginate_by=30,
            template_name="mpa/Mpa_list.html",
        ),
        name="mpa-siteslist",
    ),
    re_path(
        r"^sites/all/$",
        ListView.as_view(
            queryset=mpas_norejects_nogeom.order_by("name"),
            context_object_name="mpa_list",
            # paginate_by=30,
            template_name="mpa/Mpa_list.html",
        ),
        name="mpa-siteslistall",
    ),
    re_path(
        r"^sites/proposed/$",
        ListView.as_view(
            queryset=mpas_proposed_nogeom.order_by("name"),
            context_object_name="mpa_list",
            # paginate_by=30,
            template_name="mpa/Mpa_list.html",
        ),
        name="mpa-siteslistall",
    ),
    re_path(
        r"^sites/json/$",
        MpaJsonListView.as_view(
            queryset=mpas_norejects_nogeom.order_by("name").only(
                "name",
                "designation_eng",
                "country",
                "status",
                "mpa_id",
                "site",
                "point_within",
                "bbox_lowerleft",
                "bbox_upperright",
            ),
            context_object_name="mpa_list",
            paginate_by=None,
            template_name="mpa/Mpa_list.json",
        ),
        name="mpa-siteslistjson",
    ),
    re_path(
        r"^sites/ids/$",
        MpaJsonListView.as_view(
            # queryset=mpas_noproposed_nogeom.order_by('mpa_id').only('mpa_id'),
            queryset=mpas_norejects_nogeom.only("mpa_id"),
            context_object_name="mpa_list",
            paginate_by=None,
            template_name="mpa/Mpa_id_list.json",
        ),
        name="mpa-siteslistjson",
    ),
    re_path(
        r"^sites/(?P<pk>\d+)/$",
        DetailView.as_view(
            model=Mpa,
            queryset=mpas_all_nogeom,
            context_object_name="mpa",
            template_name="mpa/Mpa_detail.html",
        ),
        name="mpa-siteinfo",
    ),
    re_path(
        r"^sites/(?P<pk>\d+)/json/$",
        MpaJsonView.as_view(
            model=Mpa,
            queryset=mpas_all_nogeom,
            context_object_name="mpa",
        ),
        name="mpa-infojson",
    ),
    re_path(r"^sites/(?P<pk>\d+)/features/$", get_mpa_geom_json, name="mpa-geojson"),
    re_path(r"^sites/(?P<pk>\d+)/edit/$", edit_mpa, name="mpa-editsite"),
    re_path(r"^sites/(?P<pk>\d+)/edit/geo/$", edit_mpa_geom, name="mpa-editsitegeom"),
    re_path(r"^lookup/point/$", lookup_point),
    re_path(
        r"^proposed/$",
        MpaListView.as_view(
            queryset=mpas_proposed_nogeom.order_by("name").only(
                "name",
                "designation_eng",
                "country",
                "mpa_id",
                "point_within",
                "bbox_lowerleft",
                "bbox_upperright",
            ),
            context_object_name="mpa_list",
            paginate_by=30,
            template_name="mpa/Mpa_list.html",
        ),
        name="mpa-candidate-siteslist",
    ),
    re_path(
        r"^proposed/(?P<pk>\d+)/$",
        DetailView.as_view(
            model=Mpa,
            queryset=mpas_proposed_nogeom.only(
                "name",
                "designation_eng",
                "country",
                "mpa_id",
                "point_within",
                "bbox_lowerleft",
                "bbox_upperright",
            ),
            context_object_name="mpa",
            template_name="mpa/MpaCandidate_detail.html",
        ),
        name="mpa-candidate-siteinfo",
    ),
]
