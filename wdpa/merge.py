from __future__ import print_function
from .models import WdpaPolygon, WdpaPoint, Wdpa2014Polygon, Wdpa2014Point
from mpa.models import Mpa, mpas_all_nogeom, VersionMetadata, mpa_post_save
from mpa import admin as mpa_admin # needed to kick in reversion registration

from django.contrib.auth import get_user_model

from django.db import connection, transaction
import reversion
from reversion.models import Revision

from django.contrib.gis import geos

####
# USAGE
# from wdpa import merge
# from mpa import admin as mpa_admin

# removelist = merge.getRemoveWdpaList()
# addlist = merge.getAddWdpaList()
# updatelist = merge.getUpdateWdpaList()

# existingrevisions = {}

# merge.removeMpasByWdpaId(removelist)
# merge.updateMpasFromWdpaList(ids=addlist, existingrevisions=existingrevisions)
# merge.updateMpasFromWdpaList(ids=updatelist, existingrevisions=existingrevisions)
####

UsaCodes = ['USA','UMI','VIR','PRI','ASM','GUM','MNP']

def getRemoveWdpaList():
    ####
    # Remove mpa records where the latest 2014 WDPA has removed that wdpaid number
    count = 0
    wdpa2remove = []
    mpa_wdpaid_list = mpas_all_nogeom.filter(wdpa_id__isnull=False).order_by('wdpa_id').values_list('wdpa_id', flat=True)
    poly_wdpa2014_list = Wdpa2014Polygon.objects.all().order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa2014_list = Wdpa2014Point.objects.all().order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa2014_list = list(poly_wdpa2014_list) + list(point_wdpa2014_list)
    for wdpaid in mpa_wdpaid_list:
        count += 1
        if wdpaid not in wdpa2014_list:
            # wdpaid has been removed from 2014 wdpaid
            wdpa2remove.append(wdpaid)
            print(wdpaid, ':', count, 'processed')
    return wdpa2remove

def removeMpasByWdpaId(remove_ids):
    for wdpaid in remove_ids:
        # now delete existing Mpa records for Wdpa sites that no longer exist
        stale_mpas = removeUsaFromQuerySet(Mpa.objects.filter(wdpa_id__in = remove_ids))
        stale_mpas.delete()

def getAddWdpaList():
    ####
    # Mark new WDPA 2014 records for direct import, no merge necessary
    count = 0
    wdpa2add = []
    poly_wdpa2014_list = Wdpa2014Polygon.objects.filter(marine='1').order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa2014_list = Wdpa2014Point.objects.filter(marine='1').order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa2014_list = list(poly_wdpa2014_list) + list(point_wdpa2014_list)
    
    poly_wdpa_list = WdpaPolygon.objects.order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa_list = WdpaPoint.objects.order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa_list = list(poly_wdpa_list) + list(point_wdpa_list)
    for wdpaid in wdpa2014_list:
        count += 1
        if wdpaid not in wdpa_list:
            # old record doesn't exist
            wdpa2add.append(wdpaid)
            print(wdpaid, ':', count, 'processed')
    newpolys = Wdpa2014Polygon.objects.filter(wdpaid__in=wdpa2add)
    newpoints = Wdpa2014Point.objects.filter(wdpaid__in=wdpa2add)
    newpolys.update(new=True, updateme=True)
    newpoints.update(new=True, updateme=True)
    return wdpa2add

def getUpdateWdpaList():
    ####
    # Find WDPA records that have updated fields
    count = 0
    wdpa2update = []
    querysets = (
        Wdpa2014Polygon.objects.defer(*Wdpa2014Polygon.get_geom_fields()).filter(marine='1', new=False),
        Wdpa2014Point.objects.defer(*Wdpa2014Point.get_geom_fields()).filter(marine='1', new=False)
    )
    for q in querysets: 
        for w in q:
            count += 1
            try:
                wold = WdpaPolygon.objects.defer(*WdpaPolygon.get_geom_fields()).filter(wdpaid = w.wdpaid).first() or WdpaPoint.objects.defer(*WdpaPoint.get_geom_fields()).filter(wdpaid = w.wdpaid).first()
                for field in Wdpa2014Polygon._meta.fields:
                    if field.name in ('id', 'updateme', 'new', 'no_take', 'no_tk_area', 'parent_iso3', 'gis_m_area', 'gis_area', 'shape_leng', 'shape_area', 'geom', 'geom_smerc', 'geog', 'point_within', 'point_within_geojson', 'bbox', 'bbox_geojson'):
                        continue
                    valnew = getattr(w, field.name)
                    valold = getattr(wold, field.name)
                    if valnew != valold:
                        if field.name == 'wdpa_pid' and valold == 0:
                            continue
                        # w.updateme = True
                        wdpa2update.append(w.wdpaid)
                        print(w.wdpaid, ': count', count, field.name, valnew, valold)
                        break
            except:
                raise
    updatepolys = Wdpa2014Polygon.objects.filter(wdpaid__in=wdpa2update)
    updatepoints = Wdpa2014Point.objects.filter(wdpaid__in=wdpa2update)
    updatepolys.update(updateme=True)
    updatepoints.update(updateme=True)
    return wdpa2update

def removeUsaFromQuerySet(qs=None):
    if qs is None:
        qs = Mpa.objects.all().defer(*Mpa.get_geom_fields())
    return qs.exclude(country__in=UsaCodes)

def updateMpasFromWdpaList(ids=[], existingrevisions={}):
    points = Wdpa2014Point.objects.filter(wdpaid__in=ids).defer(*Wdpa2014Point.get_geom_fields()).order_by('wdpaid')
    polys = Wdpa2014Polygon.objects.filter(wdpaid__in=ids).defer(*Wdpa2014Polygon.get_geom_fields()).order_by('wdpaid')
    updateMpasFromWdpaQueryset(qs=points, poly=False, existingrevisions=existingrevisions)
    updateMpasFromWdpaQueryset(qs=polys, poly=True, existingrevisions=existingrevisions)
    return existingrevisions


def updateMpasFromWdpaQueryset(qs=None, poly=True, existingrevisions={}):
    if qs is None:
        qs = Wdpa2014Polygon.objects.all().defer(*Wdpa2014Polygon.get_geom_fields()).order_by('wdpaid')
    count = 0
    for wpoly in qs:
        # mpa, created = Mpa.objects.get_or_create(wdpa_id=wpoly.wdpaid)
        created = False
        try:
            mpa = Mpa.objects.get(wdpa_id=wpoly.wdpaid)
            if mpa.country in UsaCodes:
                print('USA: not processing', wpoly.wdpaid)
                continue
        except Mpa.DoesNotExist:
            mpa = Mpa(wdpa_id=wpoly.wdpaid)
            created = True
        count += 1
        print(count)
        try:
            versions = len(reversion.get_for_object(mpa))
        except:
            versions = 0
        if versions > 0:
            print('Previous versions for wdpaid', wpoly.wdpaid)
            existingrevisions[wpoly.wdpaid] = (
                {
                    'no_take_old': mpa.no_take,
                    'no_take_area_old': mpa.no_take_area
                },
                {
                    'no_take': wpoly.no_take,
                    'no_take_area': wpoly.no_tk_area
                }
            )
        else:
            print('Updating wdpaid', wpoly.wdpaid)
        # update record and create a revision so we can roll back if needed
        with transaction.atomic(), reversion.create_revision():
            updateMpaFromWdpa(wpoly, mpa, poly)
            comment = 'Updated record from WDPA October 2014'
            reference = 'World Database on Protected Areas, October 2014'
            reversion.set_comment(comment)
            User = get_user_model()
            user = User.objects.get(username='russmo')
            reversion.set_user(user)
            reversion.add_meta(VersionMetadata, comment=comment, reference=reference)
    return True
     

def updateMpaFromWdpa(wpoly, mpa, poly=True):
    mpa.is_point = False
    if not poly:
        mpa.is_point = True
        if mpa.geom:
            # existing mpa has geom, so don't use this point
            mpa.is_point = False
    mpa.name = wpoly.name
    mpa.wdpa_id = wpoly.wdpaid
    mpa.country = wpoly.country
    mpa.sovereign = wpoly.parent_iso3 # add this to mpa model!!!
    mpa.sub_location = wpoly.sub_loc
    mpa.designation = wpoly.desig
    mpa.designation_eng = wpoly.desig_eng
    mpa.designation_type = wpoly.desig_type
    mpa.iucn_category = wpoly.iucn_cat
    mpa.int_criteria = wpoly.int_crit
    mpa.marine = wpoly.marine
    mpa.status = wpoly.status
    mpa.status_year = wpoly.status_yr
    mpa.rep_m_area = wpoly.rep_m_area
    mpa.rep_area = wpoly.rep_area
    mpa.gov_type = wpoly.gov_type
    mpa.mgmt_auth = wpoly.mang_auth
    mpa.mgmt_plan_ref = wpoly.mang_plan
    mpa.no_take = wpoly.no_take
    mpa.no_take_area = wpoly.no_tk_area

    if poly:
        mpa.calc_m_area = wpoly.gis_m_area
        mpa.calc_area = wpoly.gis_area
        newgeom = wpoly.geom.clone()
        try:
            newgeom = newgeom.buffer(0)
        except:
            pass
        try:
            newgeom = geos.MultiPolygon(newgeom)
        except:
            pass
        mpa.geom = newgeom

    else:
        mpa.point_geom = wpoly.geom
    
    mpa.save()
    # mpa_post_save(sender=Mpa, instance=mpa)

