from django.urls import path, re_path, include
from django.views.generic import TemplateView, DetailView, ListView
from category.views import CategoryDetailView, CategoryGeoJsonView

from category.models import Category, Details


urlpatterns = [
    # Examples:
    # re_path(r'^$', 'mpatlas.views.home', name='home'),
    # re_path(r'^mpatlas/', include('mpatlas.foo.urls')),
    # re_path(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='index_demo.html')),
    # re_path(r'^sites/', 'wdpa.views.sitelist'),
    # re_path(r'^sites/(?P<siteid>\d)/$', 'wdpa.views.siteinfo'),
    # re_path(r'^map/$', 'campaign.views.map'),
    re_path(
        r"^list/$",
        ListView.as_view(
            queryset=Category.objects.all().order_by("name"),
            context_object_name="category_list",
            paginate_by=60,
            template_name="category/Category_list.html",
        ),
        name="category-list",
    ),
    # re_path(r'list/geojson/$',
    #     JsonListView.as_view(
    #         queryset=Campaign.objects.filter(point_geom__isnull=False).order_by('name'),
    #         context_object_name='campaign_list',
    #         paginate_by=None,
    #         template_name='campaign/Campaign_list_geojson.json'),
    #     name='campaign-list-geojson'),
    re_path(
        r"^(?P<pk>\d+)/$",
        CategoryDetailView.as_view(
            model=Category,
            queryset=Category.objects.all().order_by("name"),
            context_object_name="category",
            template_name="category/Category_detail.html",
        ),
        name="category-info-byid",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/$",
        CategoryDetailView.as_view(
            model=Category,
            queryset=Category.objects.all().order_by("name"),
            context_object_name="category",
            template_name="category/Category_detail.html",
        ),
        name="category-info",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/features/$",
        CategoryGeoJsonView.as_view(
            model=Category,
            queryset=Category.objects.all().order_by("name"),
            context_object_name="category",
        ),
        name="category-geojson",
    ),
    # re_path(r'^(?P<pk>\d+)/point/$', 'campaign.views.get_campaign_pointgeom_json', name='campaign-point-geojson'),
    # re_path(r'^initiative/(?P<pk>\d+)/$',
    #     DetailView.as_view(
    #         model=Initiative,
    #         queryset=Initiative.objects.all().order_by('name'),
    #         context_object_name='initiative',
    #         template_name='campaign/Initiative_detail.html'),
    #     name='initiative-info-byid'),
    # re_path(r'^initiative/(?P<slug>[\w-]+)/$',
    #     DetailView.as_view(
    #         model=Initiative,
    #         queryset=Initiative.objects.all().order_by('name'),
    #         context_object_name='initiative',
    #         template_name='campaign/Initiative_detail.html'),
    #     name='initiative-info'),
    # re_path(r'^(?P<pk>\d+)/edit/$', 'campaign.views.edit_campaign', name='campaign-edit'),
    # re_path(r'^lookup/point/$', 'mpa.views.lookup_point'),
]
