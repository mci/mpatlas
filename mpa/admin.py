from django.contrib.gis import admin
from django.forms.models import fields_for_model
import reversion
from models import Mpa, WikiArticle, Contact, CandidateInfo

class WikiArticleInline(admin.StackedInline):
    model = WikiArticle

class CandidateInfoInline(admin.StackedInline):
    model = CandidateInfo

def get_fields_missing_from_fieldsets(fieldsets, fields):
    missing_fields = list(fields)
    for fieldset in fieldsets:
        if fieldset[1]['fields']:
            for field in fieldset[1]['fields']:
                if field in missing_fields:
                    missing_fields.remove(field)
    return missing_fields

class MpaAdmin(reversion.VersionAdmin, admin.GeoModelAdmin):
    list_display = ('name', 'english_designation', 'mpa_id', 'wdpa_id', 'country', 'sub_location', 'colored_verification_state')
    search_fields = ['name', 'country', 'sub_location', 'mpa_id', 'wdpa_id']
    fieldsets = [
        ('Protected Area Name', {'fields': ['name', 'designation', 'designation_eng', 'long_name', 'short_name', 'slug']}),
        ('Categories/Tags', {'fields': ['categories']}),
        ('Is this a Marine Protected Area or a different marine managed area?', {'fields': ['is_mpa']}),
        ('Status', {'fields': ['status', 'status_year', 'implemented', 'implementation_date', 'verification_state', 'verification_reason', 'verified_by', 'verified_date']}),
        ('Summary Information', {'fields': ['summary']}),
        ('Designation Type', {'fields': ['designation_type', 'int_criteria', 'iucn_category']}),
        ('Region, Jurisdiction & Management', {'fields': ['sovereign', 'country', 'sub_location', 'gov_type', 'mgmt_auth', 'mgmt_plan_type', 'mgmt_plan_ref']}),
        ('Points of Contact', {'fields': ['contact', 'other_contacts']}),
        ('Boundaries', {'fields': ['is_point']}),
        ('Permanence and Constancy', {'fields': ['permanence', 'permanence_citation', 'constancy', 'constancy_citation']}),
        ('Fishing Restrictions', {'fields': ['fishing', 'fishing_info', 'fishing_citation']}),
        ('Access Restrictions', {'fields': ['access', 'access_info', 'access_citation']}),
        ('Protection Focus', {'fields': ['protection_focus', 'protection_focus_info', 'protection_focus_citation', 'primary_conservation_focus', 'secondary_conservation_focus', 'tertiary_conservation_focus', 'conservation_focus_info', 'conservation_focus_citation']}),
    ]
    inlines = [
        WikiArticleInline,
        CandidateInfoInline,
    ]

    def get_fieldsets(self, request, obj=None):
            fieldsets = super(MpaAdmin, self).get_fieldsets(request, obj)
            remaining_fields = get_fields_missing_from_fieldsets(fieldsets, [f for f in fields_for_model(Mpa)])
            if remaining_fields:
                fieldsets.append( ('Additional Fields', {'fields': remaining_fields}) )
            return fieldsets

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
