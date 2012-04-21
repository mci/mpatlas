from django.contrib.gis import admin
import reversion
from models import Mpa, MpaCandidate, WikiArticle, Contact

class WikiArticleInline(admin.StackedInline):
    model = WikiArticle

class MpaAdmin(reversion.VersionAdmin, admin.GeoModelAdmin):
    list_display = ('name', 'mpa_id', 'wdpa_id', 'country')
    search_fields = ['name', 'country', 'mpa_id', 'wdpa_id']
    inlines = [
        WikiArticleInline,
    ]

admin.site.register(Mpa, MpaAdmin)
#admin.site.register(WikiArticle, reversion.VersionAdmin)
admin.site.register(Contact, reversion.VersionAdmin)
admin.site.register(MpaCandidate, admin.GeoModelAdmin)
