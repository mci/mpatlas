from django.contrib.gis import admin
from .models import Wdpa2019Poly, Wdpa2019Point
from .models import Wdpa2018Poly, Wdpa2018Point
from .models import WdpaPolygon, WdpaPoint, Wdpa2014Polygon, Wdpa2014Point

class WdpaAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'wdpaid', 'iso3')
    search_fields = ['name', 'iso3', 'wdpaid']

admin.site.register(Wdpa2019Poly, WdpaAdmin)
admin.site.register(Wdpa2019Point, WdpaAdmin)

admin.site.register(Wdpa2018Poly, WdpaAdmin)
admin.site.register(Wdpa2018Point, WdpaAdmin)

admin.site.register(WdpaPolygon, WdpaAdmin)
admin.site.register(WdpaPoint, WdpaAdmin)
admin.site.register(Wdpa2014Polygon, WdpaAdmin)
admin.site.register(Wdpa2014Point, WdpaAdmin)