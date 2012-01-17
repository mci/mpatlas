from django.contrib.gis import admin
from models import EezSimplified

admin.site.register(EezSimplified, admin.GeoModelAdmin)
