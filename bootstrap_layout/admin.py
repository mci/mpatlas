from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminRadioSelect

from .models import Section, CONTAINER_CHOICES

'''
class SectionForm(forms.ModelForm):
    # container = forms.ChoiceField(choices=CONTAINER_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Section
        widgets = {
           'container': forms.RadioSelect,
        }
        # fields = ['container']
        fields = '__all__'

class SectionAdmin(admin.ModelAdmin):
    model = Section
    radio_fields = { 'container': admin.VERTICAL }

admin.site.register(Section, SectionAdmin)
'''