from django.contrib import admin
from .models import Category, Details, TaggedItem


class DetailsInline(admin.StackedInline):
    model = Details


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class CategoryAdmin(admin.ModelAdmin):
    inlines = [DetailsInline, TaggedItemInline]


admin.site.register(Category, CategoryAdmin)
