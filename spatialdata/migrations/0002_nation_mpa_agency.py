# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spatialdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nation',
            name='mpa_agency',
            field=ckeditor.fields.RichTextField(null=True, verbose_name=b'National Marine Protected Area Agency', blank=True),
            preserve_default=True,
        ),
    ]
