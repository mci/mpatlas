from django.contrib.gis import admin
from models import WdpaPolygon, WdpaPoint

admin.site.register(WdpaPolygon, admin.GeoModelAdmin)
admin.site.register(WdpaPoint, admin.GeoModelAdmin)
