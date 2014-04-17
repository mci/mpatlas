from django.contrib.gis import admin
import reversion
from models import Mpa, WikiArticle, Contact, CandidateInfo

class WikiArticleInline(admin.StackedInline):
    model = WikiArticle

class CandidateInfoInline(admin.StackedInline):
    model = CandidateInfo

class MpaAdmin(reversion.VersionAdmin, admin.GeoModelAdmin):
    list_display = ('name', 'english_designation', 'mpa_id', 'wdpa_id', 'country', 'sub_location', 'colored_verification_state')
    search_fields = ['name', 'country', 'sub_location', 'mpa_id', 'wdpa_id']
    inlines = [
        WikiArticleInline,
        CandidateInfoInline,
    ]

    def english_designation(self, obj):
    	if (obj.designation == obj.designation_eng):
    		return obj.designation
    	else:
    		return '%s (%s)' % (obj.designation, obj.designation_eng)
    english_designation.admin_order_field = 'designation'
    english_designation.short_description = 'Designation'

    def colored_verification_state(self, obj):
    	if (obj.verification_state == 'Rejected as MPA'):
    		color_code = 'f00'
    	else:
    		color_code = '000'
        return '<span style="color: #%s;">%s</span>' % (color_code, obj.verification_state)
    colored_verification_state.allow_tags = True
    colored_verification_state.admin_order_field = 'verification_state'
    colored_verification_state.short_description = 'Verification state'

admin.site.register(Mpa, MpaAdmin)
admin.site.register(Contact, reversion.VersionAdmin)
# admin.site.register(WikiArticle, reversion.VersionAdmin)
# admin.site.register(MpaCandidate, admin.GeoModelAdmin)
