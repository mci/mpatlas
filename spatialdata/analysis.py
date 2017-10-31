from __future__ import print_function
from .models import Eez, EezMembership
from wdpa.models import WdpaPolygon
from django.db import connection, transaction

def findMpasInEez(simplified=False):
    for eez in Eez.objects.only('id'):
        print('Eez:', eez.eez)
        if (simplified):
            mpas = WdpaPolygon.objects.only('id').filter(geom__relate=(eez.simple_geom, 'T********'))
        else:
            mpas = WdpaPolygon.objects.only('id').filter(geom__relate=(eez.geom, 'T********'))
        for mpa in mpas.iterator():
            cursor = connection.cursor()
            cursor.execute("SELECT ST_Area(ST_Intersection(mpa.geog, eez.geog), true) AS interarea FROM %s as mpa, %s as eez WHERE mpa.id = %%s AND eez.id = %%s" % (mpa._meta.db_table, eez._meta.db_table), [mpa.pk, eez.pk])
            try:
                area = cursor.fetchone()[0]
            except:
                area = None
            transaction.rollback_unless_managed()
            mpamember = EezMembership(eez=eez, mpa=mpa, area_in_eez=area)
            mpamember.save()
            print(mpa.name, ':', area/1000000, "km^2")

def findMpasInEezRaw(simplified=False):
    for eez in Eez.objects.only('id'):
        print('Eez:', eez.eez)
        mpas = WdpaPolygon.objects.only('id').filter(geom__relate=(eez.geom, 'T********'))
        cursor = connection.cursor()
        try:
            if (simplified):
                try:
                    cursor.execute("SELECT mpa.id FROM %s as mpa, %s as eez WHERE eez.id = %%s AND ST_Relate(mpa.geom, eez.simple_geom, 'T********')" % (WdpaPolygon._meta.db_table, eez._meta.db_table), [eez.pk])
                except:
                    transaction.rollback_unless_managed()
                    simplified = False
            if (not simplified):
                cursor.execute("SELECT mpa.id FROM %s as mpa, %s as eez WHERE eez.id = %%s AND ST_Relate(mpa.geom, eez.geom, 'T********')" % (WdpaPolygon._meta.db_table, eez._meta.db_table), [eez.pk])
            for mpaid in [r[0] for r in cursor.fetchall()]:
                mpa = WdpaPolygon.objects.get(pk=mpaid)
                cursor = connection.cursor()
                cursor.execute("SELECT ST_Area(ST_Intersection(mpa.geog, eez.geog), true) AS interarea FROM %s as mpa, %s as eez WHERE mpa.id = %%s AND eez.id = %%s" % (mpa._meta.db_table, eez._meta.db_table), [mpa.pk, eez.pk])
                try:
                    area = cursor.fetchone()[0]
                except:
                    area = None
                mpamember = EezMembership(eez=eez, mpa=mpa, area_in_eez=area)
                mpamember.save()
                transaction.commit_unless_managed()
                print(mpa.name, ':', area/1000000, "km^2")
        except:
            transaction.rollback_unless_managed()