# Generated by Django 2.2.17 on 2020-12-21 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wdpa', '0007_auto_20201221_1716'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wdpa2014Point',
        ),
        migrations.DeleteModel(
            name='Wdpa2014Polygon',
        ),
        migrations.DeleteModel(
            name='Wdpa2018Point',
        ),
        migrations.DeleteModel(
            name='Wdpa2018Poly',
        ),
        migrations.DeleteModel(
            name='WdpaPoint_old',
        ),
        migrations.DeleteModel(
            name='WdpaPolygon_old',
        ),
    ]
