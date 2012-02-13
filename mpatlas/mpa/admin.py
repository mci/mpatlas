from django.contrib.gis import admin
from models import Mpa, MpaCandidate

admin.site.register(Mpa, admin.GeoModelAdmin)
admin.site.register(MpaCandidate, admin.GeoModelAdmin)
