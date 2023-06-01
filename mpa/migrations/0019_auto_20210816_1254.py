# Generated by Django 3.1.7 on 2021-08-16 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpa', '0018_auto_20201221_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mpa',
            name='datasource',
        ),
        migrations.AddField(
            model_name='mpa',
            name='datasources',
            field=models.JSONField(default=dict, verbose_name='Data Sources'),
        ),
        migrations.AlterField(
            model_name='mpa',
            name='fishing_protection_details',
            field=models.JSONField(default=dict, editable=False, verbose_name='Fishing Protection Level Details'),
        ),
        migrations.AlterField(
            model_name='mpa',
            name='protection_mpaguide_details',
            field=models.JSONField(default=dict, editable=False, verbose_name='Protection Level Details - MPA Guide'),
        ),
        migrations.AlterField(
            model_name='mpa',
            name='protection_rbcs_details',
            field=models.JSONField(default=dict, editable=False, verbose_name='Protection Level Details - RBCS'),
        ),
        migrations.DeleteModel(
            name='DataSource',
        ),
    ]