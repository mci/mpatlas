from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from models import Campaign, Initiative
from django.utils.html import strip_tags

class CampaignAdmin(geoadmin.OSMGeoAdmin):
    raw_id_fields = ('mpas',)
    list_display = ('name', 'country', 'initiative_list', 'summary_excerpt')
    search_fields = ['name', 'country', 'summary', 'initiative__name']

    def summary_excerpt(self, obj):
        if (obj.summary):
            return strip_tags(obj.summary[:50]) + '...'
        else:
            return ''
    summary_excerpt.admin_order_field = 'summary'
    summary_excerpt.short_description = 'Summary (excerpt)'

    def initiative_list(self, obj):
        return ', '.join(obj.initiative_set.values_list('name', flat=True))
    # initiative_list.admin_order_field = 'initiative_list'
    initiative_list.short_description = 'Initiatives'

class InitiativeAdmin(geoadmin.OSMGeoAdmin):
    pass

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Initiative, InitiativeAdmin)