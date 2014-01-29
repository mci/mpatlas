from django.contrib.gis import admin
from models import Campaign

admin.site.register(Campaign, admin.OSMGeoAdmin)