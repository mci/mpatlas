from django.contrib.gis import admin
from .models import Nation, Eez

class NationAdmin(admin.GeoModelAdmin):
    list_display = ('name',)

admin.site.register(Eez, admin.GeoModelAdmin)
admin.site.register(Nation, NationAdmin)