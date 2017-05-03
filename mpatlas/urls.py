from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.views.generic import RedirectView
# from wiki.urls import get_pattern as get_wiki_pattern
# from django_notify.urls import get_pattern as get_notify_pattern
from django.views.decorators.cache import cache_page, never_cache

from views import MapView

from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
admin.autodiscover()

def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


urlpatterns = [
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^users/', include('accounts.urls')),
    # url(r'socialauth/', include('social_auth.urls')),
    
    url(r'^mpa/', include('mpa.urls')),
    url(r'^campaign/', include('campaign.urls')),
    url(r'^category/', include('category.urls')),
    url(r'^region/', include('spatialdata.urls')),
    
    url(r'^news/', TemplateView.as_view(template_name='news.html')),

    url(r'^explore/$', cache_page(60*1)(MapView.as_view(template_name='map.html'))),
    url(r'^dev/map/$', cache_page(60*1)(MapView.as_view(template_name='v3_map.html'))),
    
    # url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='home.html')),

    url(r'^learn/mpapedia/(?P<extrapath>.*)$', RedirectView.as_view(url='/learn/%(extrapath)s', permanent=True)),
    # Only redirect the top level /learn/ to mpapedia
    # url(r'^learn/$', RedirectView.as_view(url='/learn/mpapedia/', permanent=False)),
    # url(r'^learn/notify/', get_notify_pattern()),
    # url(r'^learn/mpapedia/', get_wiki_pattern()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/jsi18n/', i18n_javascript),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('cms.urls')),

    prefix_default_language=False
)

