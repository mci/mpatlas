from django.contrib.gis import admin
from .models import WdpaSource
from .models import WdpaPoly_new, WdpaPoint_new
from .models import WdpaPoly_prev, WdpaPoint_prev

# from .models import Wdpa2018Poly, Wdpa2018Point
# from .models import WdpaPolygon, WdpaPoint, Wdpa2014Polygon, Wdpa2014Point


class WdpaSourceAdmin(admin.GISModelAdmin):
    list_display = ("metadataid", "year", "update_yr", "data_title", "resp_party")
    search_fields = [
        "metadataid",
        "year",
        "update_yr",
        "data_title",
        "resp_party",
        "citation",
    ]


class WdpaAdmin(admin.GISModelAdmin):
    list_display = ("name", "wdpaid", "iso3")
    search_fields = ["name", "iso3", "wdpaid"]


admin.site.register(WdpaSource, WdpaSourceAdmin)

admin.site.register(WdpaPoly_new, WdpaAdmin)
admin.site.register(WdpaPoint_new, WdpaAdmin)

admin.site.register(WdpaPoly_prev, WdpaAdmin)
admin.site.register(WdpaPoint_prev, WdpaAdmin)

# admin.site.register(Wdpa2018Poly, WdpaAdmin)
# admin.site.register(Wdpa2018Point, WdpaAdmin)

# admin.site.register(WdpaPolygon, WdpaAdmin)
# admin.site.register(WdpaPoint, WdpaAdmin)
# admin.site.register(Wdpa2014Polygon, WdpaAdmin)
# admin.site.register(Wdpa2014Point, WdpaAdmin)
