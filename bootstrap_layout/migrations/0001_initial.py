# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 13:43
from __future__ import unicode_literals

import bootstrap_layout.models
from django.db import migrations, models
import django.db.models.deletion
import djangocms_attributes_field.fields
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0007_auto_20161016_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='bootstrap_layout_section', serialize=False, to='cms.CMSPlugin')),
                ('bg_size', models.CharField(choices=[('fit width: 100% auto', '100% auto'), ('fit height: auto 100%', 'auto 100%'), ('fill: cover ', 'cover'), ('default: auto', 'auto')], default='cover', max_length=25, verbose_name='Background Size')),
                ('bg_position', models.CharField(blank=True, default='center', max_length=25, verbose_name='Background Position')),
                ('bg_repeat', models.CharField(blank=True, choices=[('no-repeat', 'no-repeat'), ('repeat', 'repeat'), ('repeat-x', 'repeat-x'), ('repeat-y', 'repeat-y')], default='no-repeat', max_length=25, verbose_name='Background Repeat')),
                ('bg_attachment', models.CharField(blank=True, choices=[('scroll', 'scroll'), ('fixed', 'fixed')], default='scroll', max_length=25, verbose_name='Background Attachment')),
                ('bg_color', models.CharField(default='transparent', help_text='(e.g., #RRGGBB, rgba(120,120,120,0.3))', max_length=25, verbose_name='CSS Background Color')),
                ('add_container', models.BooleanField(default=True, help_text='Adds a ".container" element inside the section', verbose_name='Add .container element')),
                ('classes', bootstrap_layout.models.Classes(blank=True, default='', help_text='Space separated classes that are added to the class. See <a href="http://getbootstrap.com/css/" target="_blank">Bootstrap 3 documentation</a>.', verbose_name='Classes')),
                ('attributes', djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Attributes')),
                ('bg_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'filer.Image')),
                ('min_height', models.CharField(default='0px', help_text='0 is default. Set it larger to expand height of section.', max_length=25, verbose_name='Minimum Section Height')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
