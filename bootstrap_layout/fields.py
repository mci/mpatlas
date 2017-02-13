# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import django.forms.fields
from django.forms.widgets import Textarea

class Classes(django.forms.fields.CharField):
    widget = django.forms.widgets.Textarea