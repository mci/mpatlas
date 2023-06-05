from django.urls import path, re_path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.views.generic import RedirectView

# from wiki.urls import get_pattern as get_wiki_pattern
# from django_notify.urls import get_pattern as get_notify_pattern
from django.views.decorators.cache import cache_page, never_cache
from django import VERSION as DJANGO_VERSION

from .views import MapView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin

admin.autodiscover()


def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


urlpatterns = [
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    re_path(r"^users/", include("accounts.urls")),
    # re_path(r'socialauth/', include('social_auth.urls')),
    re_path(r"^mpa/", include("mpa.urls")),
    re_path(r"^wdpa/", include("wdpa.urls")),
    re_path(r"^campaign/", include("campaign.urls")),
    re_path(r"^category/", include("category.urls")),
    re_path(r"^region/", include("spatialdata.urls")),
    # re_path(r'^news/', TemplateView.as_view(template_name='v3_news.html')),
    # re_path(r'^explore/$', cache_page(60*1)(MapView.as_view(template_name='map.html'))),
    # re_path(r'^map/$', cache_page(60*1)(MapView.as_view(template_name='v3_map.html'))),
    re_path(
        r"^map/mpas/$", cache_page(60 * 1)(MapView.as_view(template_name="v3_map.html"))
    ),
    # re_path(r'^(index\.htm(l)?)?$', TemplateView.as_view(template_name='home.html')),
    re_path(
        r"^learn/mpapedia/(?P<extrapath>.*)$",
        RedirectView.as_view(url="/learn/%(extrapath)s", permanent=True),
    ),
    # Only redirect the top level /learn/ to mpapedia
    # re_path(r'^learn/$', RedirectView.as_view(url='/learn/mpapedia/', permanent=False)),
    re_path(r"^explore/$", RedirectView.as_view(url="/map/mpas/", permanent=False)),
    # re_path(r'^learn/notify/', get_notify_pattern()),
    # re_path(r'^learn/mpapedia/', get_wiki_pattern()),
    re_path(
        r"^en-us/(?P<extrapath>.*)$",
        RedirectView.as_view(url="/%(extrapath)s", permanent=False),
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += i18n_patterns(
    # Uncomment the admin/doc line below to enable admin documentation:
    re_path(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    # Uncomment the next line to enable the admin:
    re_path(r"^admin/jsi18n/", i18n_javascript),
    re_path(
        r"^admin/",
        include(admin.site.urls) if DJANGO_VERSION <= (2, 0) else admin.site.urls,
    ),
    re_path(r"^", include("cms.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
