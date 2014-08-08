from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from models import Campaign, Initiative

class CampaignAdmin(geoadmin.OSMGeoAdmin):
	raw_id_fields = ('mpas',)

class InitiativeAdmin(geoadmin.OSMGeoAdmin):
	pass

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Initiative, InitiativeAdmin)