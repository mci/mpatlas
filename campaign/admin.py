from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from .models import Campaign, Initiative, Organization
from django.utils.html import strip_tags


class CampaignAdmin(geoadmin.GISModelAdmin):
    raw_id_fields = ("mpas",)
    list_display = ("name", "country", "initiative_list", "summary_excerpt")
    search_fields = ["name", "country", "summary", "initiative__name"]
    ordering = ("name",)

    def summary_excerpt(self, obj):
        if obj.summary:
            return strip_tags(obj.summary[:50]) + "..."
        else:
            return ""

    summary_excerpt.admin_order_field = "summary"
    summary_excerpt.short_description = "Summary (excerpt)"

    def initiative_list(self, obj):
        return ", ".join(obj.initiative_set.values_list("name", flat=True))

    # initiative_list.admin_order_field = 'initiative_list'
    initiative_list.short_description = "Initiatives"


class InitiativeAdmin(geoadmin.GISModelAdmin):
    list_display = ("name", "campaign_excerpt", "summary_excerpt")
    search_fields = ["name", "summary", "campaigns__name"]
    ordering = ("name",)

    def campaign_list(self, obj):
        return ", ".join(obj.campaigns.values_list("name", flat=True))

    # campaign_list.admin_order_field = 'campaign_list'
    campaign_list.short_description = "Campaigns"

    def campaign_excerpt(self, obj):
        if self.campaign_list(obj):
            return strip_tags(self.campaign_list(obj)[:50]) + "..."
        else:
            return ""

    # campaign_excerpt.admin_order_field = 'campaigns'
    campaign_excerpt.short_description = "Campaign list (excerpt)"

    def summary_excerpt(self, obj):
        if obj.summary:
            return strip_tags(obj.summary[:50]) + "..."
        else:
            return ""

    # summary_excerpt.admin_order_field = 'summary'
    summary_excerpt.short_description = "Summary (excerpt)"


class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "nickname", "website", "social_handles")
    search_fields = ["name", "nickname", "website", "social_handles", "summary"]
    ordering = ("name",)


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Initiative, InitiativeAdmin)
admin.site.register(Organization, OrganizationAdmin)
