# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.conf import settings

from . import models

class SectionPlugin(CMSPluginBase):
	model = models.Section
	name = "Website Section"
	module = 'Advanced Bootstrap Layout'
	render_template = "bootstrap_layout/section.html"
	allow_children = True
	text_enabled = False
	#raw_id_fields = ('group',)
	admin_preview = False

plugin_pool.register_plugin(SectionPlugin)