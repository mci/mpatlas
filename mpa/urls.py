from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, DetailView, ListView

from mpa.models import Mpa, MpaCandidate, mpas_all_nogeom, mpas_norejects_nogeom, mpas_noproposed_nogeom, mpas_proposed_nogeom
from mpa.views import MpaListView, MpaJsonListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    
    #url(r'^sites/', 'wdpa.views.sitelist'),
    #url(r'^sites/(?P<siteid>\d)/$', 'wdpa.views.siteinfo'),
    
    url(r'^revision/$', 'mpa.views.revision_view'),
    url(r'^revision2/$', 'mpa.views.revision_view2'),
    url(r'^sites/$',
        MpaListView.as_view(
            queryset=mpas_norejects_nogeom.order_by('name').only('name', 'designation_eng', 'country', 'mpa_id', 'point_within', 'bbox_lowerleft', 'bbox_upperright'),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='mpa-siteslist'),
    url(r'^sites/all/$',
        ListView.as_view(
            queryset=mpas_norejects_nogeom.order_by('name'),
            context_object_name='mpa_list',
            #paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='mpa-siteslistall'),
    url(r'^sites/proposed/$',
        ListView.as_view(
            queryset=mpas_proposed_nogeom.order_by('name'),
            context_object_name='mpa_list',
            #paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='mpa-siteslistall'),
    url(r'^sites/json/$',
        MpaJsonListView.as_view(
            queryset=mpas_norejects_nogeom.order_by('name').only('name', 'designation_eng', 'country', 'status', 'mpa_id', 'point_within', 'bbox_lowerleft', 'bbox_upperright'),
            context_object_name='mpa_list',
            paginate_by=None,
            template_name='mpa/Mpa_list.json'),
        name='mpa-siteslistjson'),
    url(r'^sites/ids/$',
        MpaJsonListView.as_view(
            # queryset=mpas_noproposed_nogeom.order_by('mpa_id').only('mpa_id'),
            queryset=mpas_norejects_nogeom.only('mpa_id'),
            context_object_name='mpa_list',
            paginate_by=None,
            template_name='mpa/Mpa_id_list.json'),
        name='mpa-siteslistjson'),
    url(r'^sites/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Mpa,
            queryset=mpas_all_nogeom,
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.html'),
        name='mpa-siteinfo'),
    url(r'^sites/(?P<pk>\d+)/json/$',
        DetailView.as_view(
            model=Mpa,
            queryset=mpas_all_nogeom,
            context_object_name='mpa',
            template_name='mpa/Mpa_detail.json'),
        name='mpa-infojson'),
    url(r'^sites/(?P<pk>\d+)/features/$', 'mpa.views.get_mpa_geom_json', name='mpa-geojson'),
    url(r'^sites/(?P<pk>\d+)/edit/$', 'mpa.views.edit_mpa', name='mpa-editsite'),

    url(r'^sites/(?P<pk>\d+)/edit/geo/$', 'mpa.views.edit_mpa_geom', name='mpa-editsitegeom'),
    
    url(r'^lookup/point/$', 'mpa.views.lookup_point'),
    
    url(r'^proposed/$',
        MpaListView.as_view(
            queryset=mpas_proposed_nogeom.order_by('name').only('name', 'designation_eng', 'country', 'mpa_id', 'point_within', 'bbox_lowerleft', 'bbox_upperright'),
            context_object_name='mpa_list',
            paginate_by=30,
            template_name='mpa/Mpa_list.html'),
        name='mpa-candidate-siteslist'),
    url(r'^proposed/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Mpa,
            queryset=mpas_proposed_nogeom.only('name', 'designation_eng', 'country', 'mpa_id', 'point_within', 'bbox_lowerleft', 'bbox_upperright'),
            context_object_name='mpa',
            template_name='mpa/MpaCandidate_detail.html'),
        name='mpa-candidate-siteinfo'),
)
