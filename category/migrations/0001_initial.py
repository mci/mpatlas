# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summary', ckeditor.fields.RichTextField(null=True, verbose_name=b'Short Summary', blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, verbose_name=b'Description', blank=True)),
                ('category', models.OneToOneField(to='category.Category')),
            ],
            options={
                'verbose_name': 'Category Details',
                'verbose_name_plural': 'Category Details',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='category_taggeditem_tagged_items', verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='category_taggeditem_items', to='category.Category')),
            ],
            options={
                'verbose_name': 'Tagged Item',
                'verbose_name_plural': 'Tagged Items',
            },
            bases=(models.Model,),
        ),
    ]
