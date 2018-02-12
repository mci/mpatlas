# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 12:41
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('campaign', '0002_auto_20180125_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='Organization id')),
                ('name', models.CharField(max_length=254, verbose_name='Name')),
                ('nickname', models.CharField(max_length=254, verbose_name='Nickname or Acronym')),
                ('slug', models.SlugField(blank=True, max_length=254, unique=True)),
                ('website', models.URLField(blank=True, max_length=254, verbose_name='Website')),
                ('social_handles', models.CharField(blank=True, max_length=254, verbose_name='Social Media Handles')),
                ('summary', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Organization Description')),
                ('logo', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_logos', to=settings.FILER_IMAGE_MODEL, verbose_name='Organization Logo')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='logo',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaign_logos', to=settings.FILER_IMAGE_MODEL, verbose_name='Campaign Logo'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='logo',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initiative_logos', to=settings.FILER_IMAGE_MODEL, verbose_name='Initiative Logo'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='start_year',
            field=models.IntegerField(blank=True, choices=[(None, None), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)], null=True, verbose_name='Start Year'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='organizations',
            field=models.ManyToManyField(to='campaign.Organization'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='organizations',
            field=models.ManyToManyField(to='campaign.Organization'),
        ),
    ]
