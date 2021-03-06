# Generated by Django 2.2.17 on 2020-12-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpa', '0017_auto_20201202_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpa',
            name='cons_obj_wdpa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mpa',
            name='supp_info_wdpa',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='mpa',
            name='protection_rbcs_level',
            field=models.IntegerField(blank=True, choices=[(1, '1: No-Take/No-Go'), (2, '2: No-Take/Regulated Access'), (3, '3: No-Take/Unregulated Access'), (4, '4: Highly Regulated Extraction'), (5, '5: Moderately Regulated Extraction'), (6, '6: Weakly Regulated Extraction'), (7, '7: Very Weakly Regulated Extraction'), (8, '8: Unregulated Extraction'), (99, '99: Unknown')], default=99, editable=False, verbose_name='Protection Level - RBCS'),
        ),
        migrations.AlterField(
            model_name='mpa',
            name='protection_rbcs_level_name',
            field=models.CharField(blank=True, choices=[('no-take/no-go', 'No-Take/No-Go'), ('no-take/regulated access', 'No-Take/Regulated Access'), ('no-take/unregulated access', 'No-Take/Unregulated Access'), ('highly regulated extraction', 'Highly Regulated Extraction'), ('moderately regulated extraction', 'Moderately Regulated Extraction'), ('weakly regulated extraction', 'Weakly Regulated Extraction'), ('very weakly regulated extraction', 'Very Weakly Regulated Extraction'), ('unregulated extraction', 'Unregulated Extraction'), ('unknown', 'Unknown')], default='unknown', editable=False, max_length=100, verbose_name='Protection Level Name - RBCS'),
        ),
    ]
