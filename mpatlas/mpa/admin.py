from django.contrib.gis import admin
from models import MpaCandidate

admin.site.register(MpaCandidate, admin.GeoModelAdmin)
