# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 21:35
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers

from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension

class Migration(migrations.Migration):

    dependencies = [
        ('mpa', '0006_auto_20171106_2135'),
    ]

    operations = [
        UnaccentExtension(),
        TrigramExtension(),
        migrations.RunSQL([
            "DROP TEXT SEARCH CONFIGURATION IF EXISTS english_unaccent;",
            "CREATE TEXT SEARCH CONFIGURATION english_unaccent( COPY = english );",
            "ALTER TEXT SEARCH CONFIGURATION english_unaccent ALTER MAPPING FOR hword, hword_part, word WITH unaccent, english_stem;",
        ]),
        migrations.RunSQL([
            "DROP TEXT SEARCH CONFIGURATION IF EXISTS simple_unaccent;",
            "CREATE TEXT SEARCH CONFIGURATION simple_unaccent( COPY = simple );",
            "ALTER TEXT SEARCH CONFIGURATION simple_unaccent ALTER MAPPING FOR hword, hword_part, word WITH unaccent, simple;",
        ]),
        migrations.RunSQL([
            '''CREATE OR REPLACE FUNCTION f_unaccent(text)
                    RETURNS text AS
                $func$
                SELECT public.unaccent('public.unaccent', $1)  -- schema-qualify function and dictionary
                $func$  LANGUAGE sql IMMUTABLE;''',
        ]),
    ]
