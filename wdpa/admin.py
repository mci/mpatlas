from django.contrib.gis import admin
from models import WdpaPolygon, WdpaPoint, Wdpa2014Polygon, Wdpa2014Point

class WdpaAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'wdpaid', 'country')
    search_fields = ['name', 'country', 'wdpaid']

admin.site.register(WdpaPolygon, WdpaAdmin)
admin.site.register(WdpaPoint, WdpaAdmin)
admin.site.register(Wdpa2014Polygon, WdpaAdmin)
admin.site.register(Wdpa2014Point, WdpaAdmin)