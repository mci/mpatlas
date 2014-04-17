from django.contrib.gis import admin
from models import USMpaPolygon

admin.site.register(USMpaPolygon, admin.GeoModelAdmin)
