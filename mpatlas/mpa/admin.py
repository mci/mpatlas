from django.contrib.gis import admin
from models import Mpa, MpaCandidate

class MpaAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'mpa_id', 'wdpa_id', 'country')
    search_fields = ['name', 'country', 'mpa_id', 'wdpa_id']

admin.site.register(Mpa, MpaAdmin)
admin.site.register(MpaCandidate, admin.GeoModelAdmin)
