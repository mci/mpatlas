from __future__ import print_function
from .models import WdpaPolygon, WdpaPoint, Wdpa2014Polygon, Wdpa2014Point, Wdpa2018Poly, Wdpa2018Point
from mpa.models import Mpa, VersionMetadata, mpa_post_save
from mpa.views import mpas_all_nogeom
from mpa import admin as mpa_admin # needed to kick in reversion registration

from django.contrib.auth import get_user_model

from django.db import connection, transaction
from django.db.models import Q, F, Func
import reversion
from reversion.models import Revision, Version

from django.contrib.gis import geos
from django.contrib.gis.db.models.functions import Area

import json
import copy

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
#qs.exclude(country__in=UsaCodes)

# Just go through CEA focus countries first, excluding USA
# mpaset = mpas_all_nogeom.filter(
#     Q(country__icontains='MEX') | Q(country__icontains='CHL') | Q(country__icontains='IDN') | 
#     Q(country__icontains='CHN') | Q(country__icontains='JPN') | 
#     Q(sovereign__icontains='MEX') | Q(sovereign__icontains='CHL') | Q(sovereign__icontains='IDN') |
#     Q(sovereign__icontains='CHN') | Q(sovereign__icontains='JPN')
# )

# wdpa_filter = (
#     Q(iso3__icontains='MEX') | Q(iso3__icontains='CHL') | Q(iso3__icontains='IDN') | 
#     Q(iso3__icontains='CHN') | Q(iso3__icontains='JPN') | 
#     Q(parent_iso3__icontains='MEX') | Q(parent_iso3__icontains='CHL') | Q(parent_iso3__icontains='IDN') |
#     Q(parent_iso3__icontains='CHN') | Q(parent_iso3__icontains='JPN')
# )

# mpaset = mpas_all_nogeom.filter(
#     Q(country__icontains='AUS') | Q(sovereign__icontains='AUS')
# )

# wdpa_filter = (
#     Q(iso3__icontains='AUS') | Q(parent_iso3__icontains='AUS')
# )

mpaset = mpas_all_nogeom.filter(
    Q(country__icontains='FRA') | Q(sovereign__icontains='FRA')
    | Q(country__icontains='ATF') | Q(country__icontains='BLM') | Q(country__icontains='GLP')
    | Q(country__icontains='GUF') | Q(country__icontains='MAF') | Q(country__icontains='MTQ')
    | Q(country__icontains='MYT') | Q(country__icontains='NCL') | Q(country__icontains='PYF')
    | Q(country__icontains='REU') | Q(country__icontains='SHN') | Q(country__icontains='SYC')
)

wdpa_filter = (
    Q(iso3__icontains='FRA') | Q(parent_iso3__icontains='FRA')
    | Q(iso3__icontains='ATF') | Q(iso3__icontains='BLM') | Q(iso3__icontains='GLP')
    | Q(iso3__icontains='GUF') | Q(iso3__icontains='MAF') | Q(iso3__icontains='MTQ')
    | Q(iso3__icontains='MYT') | Q(iso3__icontains='NCL') | Q(iso3__icontains='PYF')
    | Q(iso3__icontains='REU') | Q(iso3__icontains='SHN') | Q(iso3__icontains='SYC')
)

def getRemoveWdpaList(verbose=False, logfile=None):
    ####
    # Remove mpa records where the latest 2018 WDPA has removed that wdpaid number
    count = 0
    wdpa2remove = []
    if logfile:
        log = open(logfile, 'w', buffering=1)
        log.write('{\n')
    mpa_wdpaid_list = mpaset.filter(wdpa_id__isnull=False, wdpa_id__gt=0).order_by('wdpa_id').values_list('wdpa_id', flat=True)
    poly_wdpa2018_list = Wdpa2018Poly.objects.all().order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa2018_list = Wdpa2018Point.objects.all().order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa2018_list = list(set(list(poly_wdpa2018_list) + list(point_wdpa2018_list)))
    for wdpaid in mpa_wdpaid_list:
        count += 1
        if wdpaid not in wdpa2018_list:
            # wdpaid has been removed from 2018 wdpaid
            wdpa2remove.append(wdpaid)
            if verbose:
                print(wdpaid, ':', count, 'processed')
            if logfile:
                for m in mpaset.filter(wdpa_id=wdpaid):
                    summary = {
                        'mpa_id': m.mpa_id,
                        'country': m.country,
                        'sovereign': m.sovereign,
                        'name': m.name,
                        'designation': m.designation,
                        'designation_eng': m.designation_eng,
                        'status': m.status,
                        'no_take': m.no_take,
                        'no_take_area': m.no_take_area,
                        'is_mpa': m.is_mpa,
                        'implemented': m.implemented,
                        'verification_state': m.verification_state
                    }
                    log.write('"%s": ' % wdpaid)
                    json.dump(summary, log, indent=4, ensure_ascii=False)
                    log.write(',\n')
                    log.flush()
    if logfile:
        log.write('\n}\n')
        log.close()
    return wdpa2remove

def removeMpasByWdpaId(remove_ids):
    for wdpaid in remove_ids:
        # now delete existing Mpa records for Wdpa sites that no longer exist
        stale_mpas = removeUsaFromQuerySet(Mpa.objects.filter(wdpa_id__in = remove_ids))
        stale_mpas.delete()

def getAddWdpaList(verbose=False):
    ####
    # Mark new WDPA 2018 records for direct import, no merge necessary
    count = 0
    wdpa2add = []
    poly_wdpa2018_list = Wdpa2018Poly.objects.filter(wdpa_filter).filter(marine__in=('1','2')).order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa2018_list = Wdpa2018Point.objects.filter(wdpa_filter).filter(marine__in=('1','2')).order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa2018_list = list(set(list(poly_wdpa2018_list) + list(point_wdpa2018_list)))
    
    poly_wdpa2014_list = Wdpa2014Polygon.objects.filter(marine='1').order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa2014_list = Wdpa2014Point.objects.filter(marine='1').order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa2014_list = list(set(list(poly_wdpa2014_list) + list(point_wdpa2014_list)))
    for wdpaid in wdpa2018_list:
        count += 1
        if wdpaid not in wdpa2014_list:
            # old record doesn't exist
            wdpa2add.append(wdpaid)
            if verbose:
                print(wdpaid, ':', count, 'processed')
    newpolys = Wdpa2018Poly.objects.filter(wdpaid__in=wdpa2add)
    newpoints = Wdpa2018Point.objects.filter(wdpaid__in=wdpa2add)
    # newpolys.update(new=True, updateme=True)
    # newpoints.update(new=True, updateme=True)
    return wdpa2add

def getAddWdpaPidList(verbose=False):
    ####
    # Mark WDPA 2018 records with new PIDs
    count = 0
    wdpa2add = []
    poly_wdpa2018_list = Wdpa2018Poly.objects.filter(wdpa_filter).filter(marine__in=('1','2')).order_by('wdpa_pid').values_list('wdpa_pid', flat=True)
    point_wdpa2018_list = Wdpa2018Point.objects.filter(wdpa_filter).filter(marine__in=('1','2')).order_by('wdpa_pid').values_list('wdpa_pid', flat=True)
    wdpa2018_list = list(set(list(poly_wdpa2018_list) + list(point_wdpa2018_list)))
    
    poly_wdpa2014_list = Wdpa2014Polygon.objects.filter(marine='1').order_by('wdpa_pid').values_list('wdpa_pid', flat=True)
    point_wdpa2014_list = Wdpa2014Point.objects.filter(marine='1').order_by('wdpa_pid').values_list('wdpa_pid', flat=True)
    wdpa2014_list = list(set(list(poly_wdpa2014_list) + list(point_wdpa2014_list)))
    for wdpa_pid in wdpa2018_list:
        try:
            w = Wdpa2018Poly.objects.filter(wdpa_filter).filter(marine__in=('1','2'), wdpa_pid=wdpa_pid).defer(*Wdpa2014Polygon.get_geom_fields()).first()
            if str(int(w.wdpaid)) == w.wdpa_pid:
                continue # we don't need this when id and pid are equal
        except:
            w = Wdpa2018Point.objects.filter(wdpa_filter).filter(marine__in=('1','2'), wdpa_pid=wdpa_pid).first()
            if str(int(w.wdpaid)) == w.wdpa_pid:
                continue # we don't need this when id and pid are equal
        count += 1
        if wdpa_pid not in wdpa2014_list:
            # old record doesn't exist
            wdpa2add.append(wdpa_pid)
            if verbose:
                print(wdpa_pid, ':', count, 'processed')
    newpolys = Wdpa2018Poly.objects.filter(wdpa_pid__in=wdpa2add)
    newpoints = Wdpa2018Point.objects.filter(wdpa_pid__in=wdpa2add)
    # newpolys.update(new=True, updateme=True)
    # newpoints.update(new=True, updateme=True)
    return wdpa2add

def getUpdateWdpaList():
    ####
    # Find WDPA records that have updated fields
    count = 0
    wdpa2update = []
    querysets = (
        Wdpa2014Polygon.objects.filter(wdpa_filter).defer(*Wdpa2014Polygon.get_geom_fields()).filter(marine='1', new=False),
        Wdpa2014Point.objects.filter(wdpa_filter).defer(*Wdpa2014Point.get_geom_fields()).filter(marine='1', new=False)
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

def diffMpaWdpa(mpa, wdpa, poly=True):
    fieldmap = {
        'name': 'name',
        'orig_name': 'orig_name',
        'country': 'iso3',
        'sovereign': 'parent_iso3',
        'sub_location': 'sub_loc',
        'designation': 'desig',
        'designation_eng': 'desig_eng',
        'status': 'status',
        'status_year': 'status_yr',
        'rep_m_area': 'rep_m_area',
        'rep_area': 'rep_area',
        'calc_area': 'gis_area',
        'calc_m_area': 'gis_m_area',
        'mgmt_plan_ref': 'mang_plan',
        'no_take': 'no_take',
        'no_take_area': 'no_tk_area',
    }
    diff = {'mpa_id': mpa.mpa_id, 'mpa': {}, 'wdpa': {}}
    for mf, wf in fieldmap.items():
        mpaval = getattr(mpa, mf)
        wdpaval = getattr(wdpa, wf)
        if mpaval != wdpaval:
            diff['mpa'][mf] = mpaval
            diff['wdpa'][mf] = wdpaval
    if poly:
        mgeom = mpa.geom
    else:
        mgeom = mpa.point_geom
    if mgeom:
        if mgeom != wdpa.geom:
            # diff['mpa']['geom'] = mgeom.geojson
            # diff['wdpa']['geom'] = wdpa.geom.geojson
            diff['mpa']['geom'] = mgeom.wkt
            diff['wdpa']['geom'] = wdpa.geom.wkt
    if len(diff['mpa'].keys()) == 0:
        diff = {}
    return diff

def updateMpasFromWdpaList(ids=[]):
    points = Wdpa2018Point.objects.filter(wdpaid__in=ids).defer(*Wdpa2018Point.get_geom_fields()).order_by('wdpaid')
    polys = Wdpa2018Poly.objects.filter(wdpaid__in=ids).defer(*Wdpa2018Poly.get_geom_fields()).order_by('wdpaid')
    updateMpasFromWdpaQueryset(qs=points, poly=False)
    updateMpasFromWdpaQueryset(qs=polys, poly=True)


def updateMpasFromWdpaQueryset(qs=None, poly=True, logfile=None, geologfile=None, dryrun=False):
    if qs is None:
        qs = Wdpa2018Poly.objects.all().defer(*Wdpa2018Poly.get_geom_fields()).order_by('wdpa_pid')
    total = max(qs.count(), Mpa.objects.filter(wdpa_pid__in=qs.values_list('wdpa_pid', flat=True).distinct()).count())
    count = 0
    diffcount = 0
    if logfile:
        log = open(logfile, 'w', buffering=1)
        log.write('{\n')
    if geologfile:
        geolog = open(geologfile, 'w', buffering=1)
        geolog.write('{\n')
    for wpoly in qs:
        # mpa, created = Mpa.objects.get_or_create(wdpa_id=wpoly.wdpaid)
        created = False
        mpas = Mpa.objects.filter(wdpa_pid=wpoly.wdpa_pid)
        if mpas.count() == 0:
            mpas = []
            mpas.append( Mpa(wdpa_pid=wpoly.wdpa_pid) )
            created = True
        else:
            if mpas[0].country in UsaCodes or wpoly.iso3 in UsaCodes:
                print('USA: not processing', wpoly.wdpa_pid)
                continue
        for mpa in mpas:
            count += 1
            print('%s/%s' % (count, total), 'adding/updating wdpa_pid', wpoly.wdpa_pid, 'with mpa_id', mpa.mpa_id)
            diff = {}
            diff_nogeom = {}
            if not created:
                diff = diffMpaWdpa(mpa, wpoly, poly)
            if diff:
                diffcount += 1
                geominfo = ''
                diff_nogeom = copy.deepcopy(diff)
                try:
                    del(diff_nogeom['mpa']['geom'])
                    del(diff_nogeom['wdpa']['geom'])
                except:
                    pass
                if 'geom' in diff['mpa']:
                    geominfo = ' and GEOM diff'
                    # Calculate area in sq km, by casting to geography first
                    try:
                        m_area_qs = mpas.filter(mpa_id=mpa.mpa_id).annotate(geog_area=Area( Func(F('geom'), function='geography', template='%(expressions)s::%(function)s') ))
                        m_area = m_area_qs.values_list('geog_area', flat=True)[0].sq_km
                    except:
                        m_area = 0
                    try:
                        w_area_qs = qs.filter(wdpa_pid=wpoly.wdpa_pid).annotate(geog_area=Area( Func(F('geom'), function='geography', template='%(expressions)s::%(function)s') ))
                        w_area = w_area_qs.values_list('geog_area', flat=True)[0].sq_km
                    except:
                        w_area=0
                    diff_nogeom['mpa']['geom_area_sqkm'] = m_area
                    diff_nogeom['wdpa']['geom_area_sqkm'] = w_area
                    diff_nogeom['mpa']['geom_area_sqkm_diff'] = abs(m_area - w_area)
                    diff_nogeom['wdpa']['geom_area_sqkm_diff'] = abs(m_area - w_area)
                    if geologfile:
                        if diffcount > 1:
                            geolog.write(',\n')
                        geolog.write('"%s": ' % wpoly.wdpa_pid)
                        json.dump(diff, geolog, indent=4, ensure_ascii=False)
                        geolog.flush()
                print('    PID:', wpoly.wdpa_pid, 'has %s field diffs %s' % (len(diff['mpa']), geominfo) )
                if logfile:
                    if diffcount > 1:
                        log.write(',\n')
                    log.write('"%s": ' % wpoly.wdpa_pid)
                    json.dump(diff_nogeom, log, indent=4, ensure_ascii=False)
                    log.flush()

            # update record and create a revision so we can roll back if needed
            if not dryrun:
                with transaction.atomic(), reversion.create_revision():
                    updateMpaFromWdpa(wpoly, mpa, poly)
                    comment = 'Updated record from WDPA September 2018'
                    reference = 'World Database on Protected Areas, September 2018'
                    reversion.set_comment(comment)
                    User = get_user_model()
                    user = User.objects.get(username='russmo')
                    reversion.set_user(user)
                    reversion.add_meta(VersionMetadata, comment=comment, reference=reference)
    if logfile:
        log.write('\n}\n')
        log.close()
    if geologfile:
        geolog.write('\n}\n')
        geolog.close()
    return True


def updateMpaFromWdpa(wpoly, mpa, poly=True):
    mpa.is_point = False
    if not poly:
        mpa.is_point = True
        if mpa.geom:
            # existing mpa has geom, so don't use this point
            mpa.is_point = False
    mpa.name = wpoly.name
    mpa.orig_name = wpoly.orig_name
    mpa.wdpa_id = int(wpoly.wdpaid)
    mpa.wdpa_pid = wpoly.wdpa_pid
    mpa.country = wpoly.iso3
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
    mpa.calc_area = wpoly.gis_area
    mpa.calc_m_area = wpoly.gis_m_area
    mpa.gov_type = wpoly.gov_type
    mpa.mgmt_auth = wpoly.mang_auth
    mpa.mgmt_plan_ref = wpoly.mang_plan
    mpa.no_take = wpoly.no_take
    mpa.no_take_area = wpoly.no_tk_area

    mpa.pa_def = wpoly.pa_def
    mpa.own_type = wpoly.own_type
    mpa.verify_wdpa = wpoly.verif

    if poly:
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

