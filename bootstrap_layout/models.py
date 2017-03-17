from __future__ import unicode_literals, absolute_import

from django.db import models

from filer.fields.image import FilerImageField
from cms.models.pluginmodel import CMSPlugin
from cms.models import Page
from cms.models.fields import PageField
from ckeditor.fields import RichTextField
#from cmsplugin_filer_image import ThumbnailOption

from . import fields
from djangocms_attributes_field.fields import AttributesField


class Classes(models.TextField):
    default_field_class = fields.Classes

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = 'Classes'
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        if 'help_text' not in kwargs:
            kwargs['help_text'] = 'Space separated classes that are added to ' + \
            	'the class. See <a href="http://getbootstrap.com/css/" ' + \
            	'target="_blank">Bootstrap 3 documentation</a>.'
        super(Classes, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Classes, self).formfield(**defaults)

SIZE_CHOICES = (
    ('100% auto', 'fit width: 100% auto'),
    ('auto 100%', 'fit height: auto 100%'),
    ('cover', 'fill: cover '),
    ('auto', 'default: auto'),
)

REPEAT_CHOICES = (
    ('no-repeat', 'no-repeat'),
    ('repeat', 'repeat'),
    ('repeat-x', 'repeat-x'),
    ('repeat-y', 'repeat-y'),
)

ATTACHMENT_CHOICES = (
    ('scroll', 'scroll'),
    ('fixed', 'fixed'),
)

CONTAINER_CHOICES = (
    ('.container', 'scroll'),
    ('.container-fluid', 'fixed'),
    ('', 'No container'),
)

class Section(CMSPlugin):
	name = models.CharField('Section Name', max_length=25, default='', help_text='Descriptive name [not rendered on page]', blank=True, null=True)
	min_height = models.CharField('Minimum Section Height', max_length=25, default='0px', help_text='0 is default. Set it larger to expand height of section.')
	bg_image = FilerImageField(blank=True, null=True)
	bg_color = models.CharField('CSS Background Color', max_length=25, default='transparent', help_text='(e.g., #RRGGBB, rgba(120,120,120,0.3))')
	bg_size = models.CharField('Background Size', max_length=25, choices=SIZE_CHOICES, default='cover')
	bg_position = models.CharField('Background Position', max_length=25, default='center', blank=True)
	bg_repeat = models.CharField('Background Repeat', max_length=25, choices=REPEAT_CHOICES, default='no-repeat', blank=True)
	bg_attachment = models.CharField('Background Attachment', max_length=25, choices=ATTACHMENT_CHOICES, default='scroll', blank=True)
	add_container = models.BooleanField('Add .container element', default=True, blank=True, help_text='Adds a ".container" element inside the section')
	# container = models.CharField('Add .container element or .container-fluid', max_length=25, choices=CONTAINER_CHOICES, default='', blank=True, help_text='Adds a ".container" or ".container-fluid" element inside the section')

	classes = Classes()

	attributes = AttributesField(
        verbose_name='Attributes',
        blank=True,
        excluded_keys=['class'],
    )

	def __unicode__(self):

		return unicode(self.name + ' ' + self.container )
