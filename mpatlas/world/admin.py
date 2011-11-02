from django.contrib.gis import admin
from world.models import WorldBorder

admin.site.register(WorldBorder, admin.GeoModelAdmin)
