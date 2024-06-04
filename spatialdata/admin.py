from django.contrib.gis import admin
from .models import Nation, Eez


class NationAdmin(admin.GISModelAdmin):
    list_display = ("name",)


admin.site.register(Eez, admin.GISModelAdmin)
admin.site.register(Nation, NationAdmin)
