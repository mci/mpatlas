# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.conf import settings

from .models import Section, CONTAINER_CHOICES

from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminRadioSelect
from django.contrib.admin.options import get_ul_class

# class SectionForm(forms.ModelForm):
#     # container = forms.ChoiceField(choices=CONTAINER_CHOICES, widget=forms.RadioSelect)
#     class Meta:
#         model = Section
#         widgets = {
#            'container': AdminRadioSelect(attrs={'class': get_ul_class(admin.HORIZONTAL),}),
#         }
#         # fields = ['container']
#         fields = '__all__'

class SectionPlugin(CMSPluginBase):
	model = Section
	radio_fields = { 'container': admin.VERTICAL }
	# form = SectionForm
	name = "Website Section"
	module = 'Advanced Bootstrap Layout'
	render_template = "bootstrap_layout/section.html"
	allow_children = True
	text_enabled = False
	#raw_id_fields = ('group',)
	admin_preview = False

plugin_pool.register_plugin(SectionPlugin)