from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from models import Campaign, Initiative

admin.site.register(Campaign, geoadmin.OSMGeoAdmin)
admin.site.register(Initiative, admin.ModelAdmin)