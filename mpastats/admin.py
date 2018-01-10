from django.contrib import admin
# from django.contrib.gis import admin
from .models import Coverage

admin.site.register(Coverage, admin.ModelAdmin)
