from django.contrib.gis import admin
from django.forms.models import fields_for_model
from reversion.admin import VersionAdmin
# import reversion
from reversion import revisions as reversion
from .models import Site, Mpa, WikiArticle, Contact, DataSource, CandidateInfo
from .views import mpas_all_nogeom
from django.db.models import When, Case, Value, F, Q, BooleanField
from django.urls import reverse
from django.utils.html import mark_safe

class WikiArticleInline(admin.StackedInline):
    model = WikiArticle

class CandidateInfoInline(admin.StackedInline):
    model = CandidateInfo

class SiteAdmin(admin.GeoModelAdmin):
    model = Site
    ordering = ['name']
    search_fields = ['name', 'orig_name', 'designation', 'designation_eng', 'wdpa_id']
    list_display = ('name', 'orig_name', 'designation', 'designation_eng', 'zones_display')
    
    def zones_display(self, obj):
        return mark_safe(", ".join([
            '<a href="%s">%s</a>' % (reverse('admin:mpa_mpa_change', args=(zone.mpa_id,)), zone.name) for zone in obj.zones.all()
        ]))
    zones_display.short_description = "Zones"

def get_fields_missing_from_fieldsets(fieldsets, fields):
    missing_fields = list(fields)
    for fieldset in fieldsets:
        if fieldset[1]['fields']:
            for field in fieldset[1]['fields']:
                if field in missing_fields:
                    missing_fields.remove(field)
    return missing_fields

# class MpaAdmin(VersionAdmin, admin.GeoModelAdmin):
class MpaAdmin(VersionAdmin, admin.GeoModelAdmin):
    # Exclude create/modify datetime fields from revisions
    def reversion_register(self, model, **options):
        options['exclude'] = ('created_date', 'modified_date',)
        super(MpaAdmin, self).reversion_register(model, **options)

    change_list_template = "mpa/admin_change_list.html"
    list_display = ('name', 'english_designation', 'mpa_id', 'wdpa_id', 'country', 'sub_location', 'has_boundary', 'colored_verification_state')
    # list_display = ('name', 'english_designation', 'mpa_id', 'wdpa_id', 'country', 'sub_location', 'colored_verification_state')
    search_fields = ['name', 'country', 'sub_location', 'mpa_id', 'wdpa_id']
    autocomplete_fields = ['site']
    fieldsets = [
        ('Parent Site', {'fields': ['site']}),
        ('Protected Area Name', {'fields': ['name', 'designation', 'designation_eng', 'long_name', 'short_name', 'slug', 'wdpa_id', 'usmpa_id', 'other_ids', 'datasource']}),
        ('Designation Type', {'fields': ['designation_type', 'int_criteria', 'iucn_category']}),
        ('Categories/Tags', {'fields': ['categories']}),
        ('Is this a Marine Protected Area or a different marine managed area?', {'fields': ['is_mpa']}),
        ('Status', {'fields': ['status', 'status_year', 'implemented', 'implementation_date', 'verification_state', 'verification_reason', 'verified_by', 'verified_date']}),
        ('Summary Information', {'fields': ['summary']}),
        ('No-Take Status & Marine Area', {'fields': ['no_take', 'no_take_area', 'rep_m_area', 'calc_m_area', 'rep_area', 'calc_area']}),
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

    def get_queryset(self, request):
        # qs = super(MpaAdmin, self).get_queryset(request).defer(*Mpa.get_geom_fields())
        qs = mpas_all_nogeom # already defined in mpa.views.mpas_all_nogeom
        # Add expression to check if boundaries exist, instead of the of pulling entire
        # geom field from database to the web server just to check if it exists
        qs = qs.annotate(
            has_boundary=Case(
                When(geom__isnull=True, then=Value(False)),
                default=Value(True),
                output_field=BooleanField()
            )
        )
        return qs

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
        return mark_safe('<span style="color: #%s;">%s</span>' % (color_code, obj.verification_state))
    colored_verification_state.allow_tags = True
    colored_verification_state.admin_order_field = 'verification_state'
    colored_verification_state.short_description = 'Verification state'

    def has_boundary(self, obj):
        if (obj.has_boundary):
            return 'True'
        else:
            return '<span style="color: #f00;">False</span>'
    has_boundary.allow_tags = True
    has_boundary.admin_order_field = 'has_boundary'
    has_boundary.short_description = 'Has Boundaries'

class ContactAdmin(VersionAdmin):
    search_fields = ['agency', 'url', 'email', 'address']

class DataSourceAdmin(VersionAdmin):
    search_fields = ['name', 'version', 'url']

admin.site.register(Site, SiteAdmin)
admin.site.register(Mpa, MpaAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(DataSource, DataSourceAdmin)
# admin.site.register(WikiArticle, VersionAdmin)
# admin.site.register(MpaCandidate, admin.GeoModelAdmin)
