from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from wiki.urls import get_pattern as get_wiki_pattern
from django_notify.urls import get_pattern as get_notify_pattern

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
admin.autodiscover()

def i18n_javascript(request):
    return admin.site.i18n_javascript(request)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpatlas.views.home', name='home'),
    # url(r'^mpatlas/', include('mpatlas.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/jsi18n/', i18n_javascript),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ckeditor/', include('ckeditor.urls')),
     
    url(r'^users/', include('accounts.urls')),
    url(r'socialauth/', include('social_auth.urls')),
    
    url(r'^mpa/', include('mpa.urls')),
    url(r'^campaign/', include('campaign.urls')),
    url(r'^region/', include('spatialdata.urls')),
    
    url(r'^news/', TemplateView.as_view(template_name='news.html')),
    
    # Only redirect the top level /learn/ to mpapedia
    #url(r'^learn/$', RedirectView.as_view(url='/learn/mpapedia/', permanent=False)),
    
    url(r'^explore/$', TemplateView.as_view(template_name='map.html')),
    
    url(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='home.html')),

    url(r'^learn/notify/', get_notify_pattern()),
    url(r'^learn/', get_wiki_pattern()),
)

