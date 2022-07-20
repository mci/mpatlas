from __future__ import print_function
# from .models import WdpaPolygon, WdpaPoint, Wdpa2014Polygon, Wdpa2014Point
from .models import WdpaPoly_prev, WdpaPoint_prev, WdpaPoly_new, WdpaPoint_new
from mpa.models import Mpa, VersionMetadata, mpa_post_save
from mpa.views import mpas_all_nogeom
from mpa import admin as mpa_admin # needed to kick in reversion registration

from django.contrib.auth import get_user_model

from django.db import connection, transaction
from django.db.models import Q, F, Func
import reversion
from reversion.models import Revision, Version

from django.contrib.gis import geos
from django.contrib.gis.db.models.functions import Area, IsValid, MakeValid

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

WDPA_POLY_NEW = WdpaPoly_new
WDPA_POINT_NEW = WdpaPoint_new
WDPA_POLY_OLD = WdpaPoly_prev
WDPA_POINT_OLD = WdpaPoint_prev

WDPA_FIELD_MAP = {
    'wdpa_id': 'wdpaid',
    'wdpa_pid': 'wdpa_pid',
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
    # WDPA fields rarely changed by MPAtlas
    'designation_type': 'desig_type',
    'iucn_category': 'iucn_cat',
    'int_criteria': 'int_crit',
    'marine': 'marine',
    'gov_type': 'gov_type',
    'own_type': 'own_type',
    'mgmt_auth': 'mang_auth',
    # WDPA fields that should never be changed by MPAtlas
    'pa_def': 'pa_def',
    'verify_wdpa': 'verif',
    'wdpa_metadataid': 'metadataid',
    'supp_info_wdpa': 'supp_info',
    'cons_obj_wdpa': 'cons_obj',
}
WDPA_FIELD_MAP_INVERSE = {v: k for k, v in WDPA_FIELD_MAP.items()}

# Try to keep original WDPA values for these fields
WDPA_RESERVED_FIELDS = (
    'pa_def',
    'metadataid',
    'verif',
    'supp_info',
    'cons_obj',
)

WDPA_GEOM_CALC_FIELDS = (
    'rep_m_area',
    'rep_area',
    'gis_area',
    'gis_m_area',
)

WDPA_USE_IF_MPA_BLANK = {
    'wdpa_id': 'wdpaid',
    'name': 'name',
    'orig_name': 'orig_name',
    'country': 'iso3',
    'sovereign': 'parent_iso3',
    'sub_location': 'sub_loc',
    'designation': 'desig',
    'designation_eng': 'desig_eng',
    'status': 'status',
    'status_year': 'status_yr',
    'mgmt_plan_ref': 'mang_plan',
    'designation_type': 'desig_type',
    'iucn_category': 'iucn_cat',
    'int_criteria': 'int_crit',
    'marine': 'marine',
    'gov_type': 'gov_type',
    'own_type': 'own_type',
    'mgmt_auth': 'mang_auth',
}

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

# wdpa_exclude = (
#     Q()
# )

mpaset = mpas_all_nogeom.exclude(
        Q(country__icontains='USA') | Q(sovereign__icontains='USA') |
        Q(country__icontains='UMI') | Q(sovereign__icontains='UMI') |
        Q(country__icontains='VIR') | Q(sovereign__icontains='VIR') |
        Q(country__icontains='PRI') | Q(sovereign__icontains='PRI') |
        Q(country__icontains='ASM') | Q(sovereign__icontains='ASM') |
        Q(country__icontains='GUM') | Q(sovereign__icontains='GUM') |
        Q(country__icontains='MNP') | Q(sovereign__icontains='MNP')
    ).filter(
        Q(country__icontains='GRC') | Q(sovereign__icontains='GRC')
    )

    # ).filter(
    #     Q(country__icontains='MEX') | Q(country__icontains='CHL') | Q(country__icontains='IDN') | 
    #     Q(country__icontains='CHN') | Q(country__icontains='JPN') | 
    #     Q(sovereign__icontains='MEX') | Q(sovereign__icontains='CHL') | Q(sovereign__icontains='IDN') |
    #     Q(sovereign__icontains='CHN') | Q(sovereign__icontains='JPN')
    # )

    # ).exclude(
    #     Q(country__icontains='MEX') | Q(country__icontains='CHL') | Q(country__icontains='IDN') | 
    #     Q(country__icontains='CHN') | Q(country__icontains='JPN') | 
    #     Q(sovereign__icontains='MEX') | Q(sovereign__icontains='CHL') | Q(sovereign__icontains='IDN') |
    #     Q(sovereign__icontains='CHN') | Q(sovereign__icontains='JPN')
    # )

wdpa_filter = (
    Q(iso3__icontains='GRC') | Q(parent_iso3__icontains='GRC')
)

# wdpa_filter = (
#     Q(iso3__icontains='MEX') | Q(iso3__icontains='CHL') | Q(iso3__icontains='IDN') | 
#     Q(iso3__icontains='CHN') | Q(iso3__icontains='JPN') | 
#     Q(parent_iso3__icontains='MEX') | Q(parent_iso3__icontains='CHL') | Q(parent_iso3__icontains='IDN') |
#     Q(parent_iso3__icontains='CHN') | Q(parent_iso3__icontains='JPN')
# )

wdpa_exclude = (
    Q(iso3__icontains='USA') | Q(parent_iso3__icontains='USA') |
    Q(iso3__icontains='UMI') | Q(parent_iso3__icontains='UMI') |
    Q(iso3__icontains='VIR') | Q(parent_iso3__icontains='VIR') |
    Q(iso3__icontains='PRI') | Q(parent_iso3__icontains='PRI') |
    Q(iso3__icontains='ASM') | Q(parent_iso3__icontains='ASM') |
    Q(iso3__icontains='GUM') | Q(parent_iso3__icontains='GUM') |
    Q(iso3__icontains='MNP') | Q(parent_iso3__icontains='MNP')
)

# mpaset = mpas_all_nogeom.filter(
#     Q(country__icontains='AUS') | Q(sovereign__icontains='AUS')
# )

# wdpa_filter = (
#     Q(iso3__icontains='AUS') | Q(parent_iso3__icontains='AUS')
# )

# mpaset = mpas_all_nogeom.filter(
#     Q(country__icontains='FRA') | Q(sovereign__icontains='FRA')
#     | Q(country__icontains='ATF') | Q(country__icontains='BLM') | Q(country__icontains='GLP')
#     | Q(country__icontains='GUF') | Q(country__icontains='MAF') | Q(country__icontains='MTQ')
#     | Q(country__icontains='MYT') | Q(country__icontains='NCL') | Q(country__icontains='PYF')
#     | Q(country__icontains='REU') | Q(country__icontains='SHN') | Q(country__icontains='SYC')
# )

# wdpa_filter = (
#     Q(iso3__icontains='FRA') | Q(parent_iso3__icontains='FRA')
#     | Q(iso3__icontains='ATF') | Q(iso3__icontains='BLM') | Q(iso3__icontains='GLP')
#     | Q(iso3__icontains='GUF') | Q(iso3__icontains='MAF') | Q(iso3__icontains='MTQ')
#     | Q(iso3__icontains='MYT') | Q(iso3__icontains='NCL') | Q(iso3__icontains='PYF')
#     | Q(iso3__icontains='REU') | Q(iso3__icontains='SHN') | Q(iso3__icontains='SYC')
# )

# mpaset = mpas_all_nogeom.filter(
#     Q(country__icontains='ZAF') | Q(sovereign__icontains='ZAF')
# )

# wdpa_filter = (
#     Q(iso3__icontains='ZAF') | Q(parent_iso3__icontains='ZAF')
# )

# mpaset = mpas_all_nogeom.filter(
#     Q(country__icontains='CAN') | Q(sovereign__icontains='CAN')
# )

# wdpa_filter = (
#     Q(iso3__icontains='CAN') | Q(parent_iso3__icontains='CAN')
# )

# mpaset = mpas_all_nogeom.filter(
#     Q(country__icontains='GBR') | Q(sovereign__icontains='GBR')
#     | Q(country__icontains='AIA') | Q(country__icontains='BMU') | Q(country__icontains='CYM')
#     | Q(country__icontains='FLK') | Q(country__icontains='GIB') | Q(country__icontains='IMN')
#     | Q(country__icontains='IOT') | Q(country__icontains='JEY') | Q(country__icontains='MSR')
#     | Q(country__icontains='PCN') | Q(country__icontains='SGS') | Q(country__icontains='SHN')
#     | Q(country__icontains='TCA') | Q(country__icontains='VGB')
# )

# wdpa_filter = (
#     Q(iso3__icontains='GBR') | Q(parent_iso3__icontains='GBR')
#     | Q(iso3__icontains='AIA') | Q(iso3__icontains='BMU') | Q(iso3__icontains='CYM')
#     | Q(iso3__icontains='FLK') | Q(iso3__icontains='GIB') | Q(iso3__icontains='IMN')
#     | Q(iso3__icontains='IOT') | Q(iso3__icontains='JEY') | Q(iso3__icontains='MSR')
#     | Q(iso3__icontains='PCN') | Q(iso3__icontains='SGS') | Q(iso3__icontains='SHN')
#     | Q(iso3__icontains='TCA') | Q(iso3__icontains='VGB')
# )

# mpaset = mpas_all_nogeom.exclude(
#         Q(country__icontains='USA') | Q(sovereign__icontains='USA') |
#         Q(country__icontains='UMI') | Q(sovereign__icontains='UMI') |
#         Q(country__icontains='VIR') | Q(sovereign__icontains='VIR') |
#         Q(country__icontains='PRI') | Q(sovereign__icontains='PRI') |
#         Q(country__icontains='ASM') | Q(sovereign__icontains='ASM') |
#         Q(country__icontains='GUM') | Q(sovereign__icontains='GUM') |
#         Q(country__icontains='MNP') | Q(sovereign__icontains='MNP')
#     ).exclude(
#         Q(country__icontains='MEX') | Q(country__icontains='CHL') | Q(country__icontains='IDN') | 
#         Q(country__icontains='CHN') | Q(country__icontains='JPN') | 
#         Q(sovereign__icontains='MEX') | Q(sovereign__icontains='CHL') | Q(sovereign__icontains='IDN') |
#         Q(sovereign__icontains='CHN') | Q(sovereign__icontains='JPN')
#     ).exclude(
#         Q(country__icontains='FRA') | Q(sovereign__icontains='FRA') |
#         Q(country__icontains='ATF') | Q(country__icontains='BLM') | Q(country__icontains='GLP') |
#         Q(country__icontains='GUF') | Q(country__icontains='MAF') | Q(country__icontains='MTQ') |
#         Q(country__icontains='MYT') | Q(country__icontains='NCL') | Q(country__icontains='PYF') |
#         Q(country__icontains='REU') | Q(country__icontains='SHN') | Q(country__icontains='SYC')
#     ).exclude(
#         Q(country__icontains='AUS') | Q(sovereign__icontains='AUS') |
#         Q(country__icontains='ZAF') | Q(sovereign__icontains='ZAF') |
#         Q(country__icontains='CAN') | Q(sovereign__icontains='CAN')
#     ).exclude(
#         Q(country__icontains='GBR') | Q(sovereign__icontains='GBR') |
#         Q(country__icontains='AIA') | Q(country__icontains='BMU') | Q(country__icontains='CYM') |
#         Q(country__icontains='FLK') | Q(country__icontains='GIB') | Q(country__icontains='IMN') |
#         Q(country__icontains='IOT') | Q(country__icontains='JEY') | Q(country__icontains='MSR') |
#         Q(country__icontains='PCN') | Q(country__icontains='SGS') | Q(country__icontains='SHN') |
#         Q(country__icontains='TCA') | Q(country__icontains='VGB')
#     )

# wdpa_filter = (
#     Q()
# )

# wdpa_exclude = (
#     Q(iso3__icontains='USA') | Q(parent_iso3__icontains='USA') |
#     Q(iso3__icontains='UMI') | Q(parent_iso3__icontains='UMI') |
#     Q(iso3__icontains='VIR') | Q(parent_iso3__icontains='VIR') |
#     Q(iso3__icontains='PRI') | Q(parent_iso3__icontains='PRI') |
#     Q(iso3__icontains='ASM') | Q(parent_iso3__icontains='ASM') |
#     Q(iso3__icontains='GUM') | Q(parent_iso3__icontains='GUM') |
#     Q(iso3__icontains='MNP') | Q(parent_iso3__icontains='MNP') |
#     Q(iso3__icontains='MEX') | Q(iso3__icontains='CHL') | Q(iso3__icontains='IDN') | 
#     Q(iso3__icontains='CHN') | Q(iso3__icontains='JPN') | 
#     Q(parent_iso3__icontains='MEX') | Q(parent_iso3__icontains='CHL') | Q(parent_iso3__icontains='IDN') |
#     Q(parent_iso3__icontains='CHN') | Q(parent_iso3__icontains='JPN') |
#     Q(iso3__icontains='FRA') | Q(parent_iso3__icontains='FRA') |
#     Q(iso3__icontains='ATF') | Q(iso3__icontains='BLM') | Q(iso3__icontains='GLP') |
#     Q(iso3__icontains='GUF') | Q(iso3__icontains='MAF') | Q(iso3__icontains='MTQ') |
#     Q(iso3__icontains='MYT') | Q(iso3__icontains='NCL') | Q(iso3__icontains='PYF') |
#     Q(iso3__icontains='REU') | Q(iso3__icontains='SHN') | Q(iso3__icontains='SYC') |
#     Q(iso3__icontains='AUS') | Q(parent_iso3__icontains='AUS') |
#     Q(iso3__icontains='ZAF') | Q(parent_iso3__icontains='ZAF') |
#     Q(iso3__icontains='CAN') | Q(parent_iso3__icontains='CAN') |
#     Q(iso3__icontains='GBR') | Q(parent_iso3__icontains='GBR') |
#     Q(iso3__icontains='AIA') | Q(iso3__icontains='BMU') | Q(iso3__icontains='CYM') |
#     Q(iso3__icontains='FLK') | Q(iso3__icontains='GIB') | Q(iso3__icontains='IMN') |
#     Q(iso3__icontains='IOT') | Q(iso3__icontains='JEY') | Q(iso3__icontains='MSR') |
#     Q(iso3__icontains='PCN') | Q(iso3__icontains='SGS') | Q(iso3__icontains='SHN') |
#     Q(iso3__icontains='TCA') | Q(iso3__icontains='VGB')
# )

def getRemoveWdpaList(verbose=False, logfile=None):
    ####
    # Remove mpa records where the latest 2019 WDPA has removed that wdpaid number
    count = 0
    wdpa2remove = []
    if logfile:
        log = open(logfile, 'w', buffering=1)
        log.write('{\n')
    mpa_wdpaid_list = mpaset.filter(wdpa_id__isnull=False, wdpa_id__gt=0).order_by('wdpa_id').values_list('wdpa_id', flat=True)
    poly_wdpa_new_list = WdpaPoly_new.objects.all().order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa_new_list = WdpaPoint_new.objects.all().order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa_new_list = list(set(list(poly_wdpa_new_list) + list(point_wdpa_new_list)))
    for wdpaid in mpa_wdpaid_list:
        count += 1
        if wdpaid not in wdpa_new_list:
            # wdpaid has been removed from 2019 wdpaid
            wdpa2remove.append(wdpaid)
            if verbose:
                print(wdpaid, ':', count, 'processed')
            if logfile:
                for m in mpaset.filter(wdpa_id=wdpaid):
                    summary = {
                        'mpa_id': m.mpa_id,
                        'wdpa_id': wdpaid,
                        'wdpa_pid': m.wdpa_pid,
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
    # now delete existing Mpa records for Wdpa sites that no longer exist
    stale_mpas = removeUsaFromQuerySet(Mpa.objects.filter(wdpa_id__in=remove_ids))
    stale_mpas.delete()

def getAddWdpaList(verbose=False):
    ####
    # Mark new WDPA 2019 records for direct import, no merge necessary
    count = 0
    wdpa2add = []
    poly_wdpa_new_list = WdpaPoly_new.objects.exclude(wdpa_exclude).filter(wdpa_filter).filter(marine__in=('1','2')).order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa_new_list = WdpaPoint_new.objects.exclude(wdpa_exclude).filter(wdpa_filter).filter(marine__in=('1','2')).order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa_new_list = list(set(list(poly_wdpa_new_list) + list(point_wdpa_new_list)))
    
    poly_wdpa_prev_list = WdpaPoly_prev.objects.filter(marine__in=('1','2')).order_by('wdpaid').values_list('wdpaid', flat=True)
    point_wdpa_prev_list = WdpaPoint_prev.objects.filter(marine__in=('1','2')).order_by('wdpaid').values_list('wdpaid', flat=True)
    wdpa_prev_list = list(set(list(poly_wdpa_prev_list) + list(point_wdpa_prev_list)))
    for wdpaid in wdpa_new_list:
        count += 1
        if wdpaid not in wdpa_prev_list:
            # old record doesn't exist
            wdpa2add.append(wdpaid)
            if verbose:
                print(wdpaid, ':', count, 'processed')
    newpolys = WdpaPoly_new.objects.filter(wdpaid__in=wdpa2add)
    newpoints = WdpaPoint_new.objects.filter(wdpaid__in=wdpa2add)
    # newpolys.update(new=True, updateme=True)
    # newpoints.update(new=True, updateme=True)
    return wdpa2add

def getAddWdpaPidList(verbose=False):
    ####
    # Mark WDPA 2019 records with new PIDs
    wdpa2add = []
    poly_wdpa_prev_list = WdpaPoly_prev.objects.filter(marine__in=('1','2')).order_by('wdpa_pid').values_list('wdpa_pid', flat=True)
    point_wdpa_prev_list = WdpaPoint_prev.objects.filter(marine__in=('1','2')).order_by('wdpa_pid').values_list('wdpa_pid', flat=True)
    wdpa_prev_list = list(set(list(poly_wdpa_prev_list) + list(point_wdpa_prev_list)))
    wpolys = WdpaPoly_new.objects.exclude(wdpa_exclude).filter(wdpa_filter).filter(
            marine__in=('1','2'),
        ).exclude(
            Q(wdpa_pid=Func(F('wdpaid'), function='INTEGER', template='(%(expressions)s::%(function)s)::text'))
        ).exclude(
            wdpa_pid__in=wdpa_prev_list
        ).values_list('wdpa_pid', flat=True)
    wpoints = WdpaPoint_new.objects.exclude(wdpa_exclude).filter(wdpa_filter).filter(
            marine__in=('1','2'),
        ).exclude(
            Q(wdpa_pid=Func(F('wdpaid'), function='INTEGER', template='(%(expressions)s::%(function)s)::text'))
        ).exclude(
            wdpa_pid__in=wdpa_prev_list
        ).only('wdpa_pid').values_list('wdpa_pid', flat=True)
    wdpa2add = wdpa2add + list(set(list(wpolys) + list(wpoints)))
    if verbose:
        print("%s wdpa_pid's processed" % (len(wdpa2add)))
        count = 0
        for a in wdpa2add:
            count += 1
            print(a, ':', count, 'processed')
    newpolys = WdpaPoly_new.objects.filter(wdpa_pid__in=wdpa2add)
    newpoints = WdpaPoint_new.objects.filter(wdpa_pid__in=wdpa2add)
    # newpolys.update(new=True, updateme=True)
    # newpoints.update(new=True, updateme=True)
    return wdpa2add


# This originally used WDPA 2012 vs 2014!!! UPDATED code to 2018 vs 2019 but not yet tested!
def getUpdateWdpaList():
    ####
    # Find WDPA records that have updated selected fields
    count = 0
    wdpa2update = []
    querysets = (
        WdpaPoly_new.objects.exclude(wdpa_exclude).filter(wdpa_filter).defer(*WdpaPoly_new.get_geom_fields()).filter(marine='1', new=False),
        WdpaPoint_new.objects.exclude(wdpa_exclude).filter(wdpa_filter).defer(*WdpaPoint_new.get_geom_fields()).filter(marine='1', new=False)
    )
    for q in querysets: 
        for w in q:
            count += 1
            try:
                wold = WdpaPoly_prev.objects.defer(*WdpaPoly_prev.get_geom_fields()).filter(wdpaid = w.wdpaid).first() or WdpaPoint_prev.objects.defer(*WdpaPoint_prev.get_geom_fields()).filter(wdpaid = w.wdpaid).first()
                for field in WdpaPoly_new._meta.fields:
                    if field.name in ('id', 'updateme', 'new', 'parent_iso3', 'gis_m_area', 'gis_area', 'shape_leng', 'shape_area', 'geom', 'geom_smerc', 'geog', 'point_within', 'point_within_geojson', 'bbox', 'bbox_geojson'):
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
    updatepolys = WdpaPoly_new.objects.filter(wdpaid__in=wdpa2update)
    updatepoints = WdpaPoint_new.objects.filter(wdpaid__in=wdpa2update)
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
        # WDPA fields rarely changed by MPAtlas
        'designation_type': 'desig_type',
        'iucn_category': 'iucn_cat',
        'int_criteria': 'int_crit',
        'marine': 'marine',
        'gov_type': 'gov_type',
        'own_type': 'own_type',
        'mgmt_auth': 'mang_auth',
        # WDPA fields that should never be changed by MPAtlas
        'pa_def': 'pa_def',
        'verify_wdpa': 'verif',
        'wdpa_metadataid': 'metadataid',
        'supp_info_wdpa': 'supp_info',
        'cons_obj_wdpa': 'cons_obj',
    }
    diff = {'mpa_id': mpa.mpa_id, 'country': wdpa.iso3 , 'sovereign': wdpa.parent_iso3 , 'mpa': {}, 'wdpa': {}}
    for mf, wf in fieldmap.items():
        mpaval = getattr(mpa, mf)
        wdpaval = getattr(wdpa, wf)
        if mf == 'pa_def':
            wdpaval = str(wdpaval).lower() in ('1', 'yes', 'true', 't')
        if mf == 'marine':
            wdpaval = int(wdpaval)
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

def diffWdpa(wdpanew, wdpaold):
    fields = (
        'pa_def',
        'name',
        'orig_name',
        'desig',
        'desig_eng',
        'desig_type',
        'iucn_cat',
        'int_crit',
        'marine',
        'no_take',
        'no_tk_area',
        'rep_m_area',
        'rep_area',
        'status',
        'status_yr',
        'gov_type',
        'own_type',
        'mang_auth',
        'mang_plan',
        'parent_iso3',
        'iso3',
        'sub_loc',
        'verif',
        'metadataid',
        'supp_info',
        'cons_obj',
    )
    diff = {'wdpa_pid': wdpanew.wdpa_pid, 'country': wdpanew.iso3 , 'sovereign': wdpanew.parent_iso3 , 'wdpa_new': {}, 'wdpa_old': {}}
    for f in fields:
        wdpanewval = getattr(wdpanew, f)
        wdpaoldval = getattr(wdpaold, f)
        if wdpanewval != wdpaoldval:
            diff['wdpa_new'][f] = wdpanewval
            diff['wdpa_old'][f] = wdpaoldval
    if wdpanew.geom != wdpaold.geom:
        diff['wdpa_new']['geom'] = wdpanew.geom.wkt
        diff['wdpa_old']['geom'] = wdpaold.geom.wkt
    if len(diff['wdpa_new'].keys()) == 0:
        diff = {}
    return diff

def updateMpasFromWdpaList(ids=[]):
    points = WdpaPoint_new.objects.filter(wdpaid__in=ids).defer(*WdpaPoint_new.get_geom_fields()).order_by('wdpaid')
    polys = WdpaPoly_new.objects.filter(wdpaid__in=ids).defer(*WdpaPoly_new.get_geom_fields()).order_by('wdpaid')
    updateMpasFromWdpaQueryset(qs=points, poly=False)
    updateMpasFromWdpaQueryset(qs=polys, poly=True)


def updateMpasFromWdpaQueryset(qs=None, poly=True, logfile=None, geologfile=None, dryrun=False):
    if qs is None:
        qs = WdpaPoly_new.objects.all().defer(*WdpaPoly_new.get_geom_fields()).order_by('wdpa_pid')
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
        if logfile:
            if count > 0:
                log.write(',\n')
            log.write('"%s": {' % wpoly.wdpa_pid)
        if geologfile:
            if count > 0:
                geolog.write(',\n')
            geolog.write('"%s": {' % wpoly.wdpa_pid)
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
        mpadiffcount = 0
        for mpa in mpas:
            count += 1
            print('%s/%s' % (count, total), 'adding/updating wdpa_pid', wpoly.wdpa_pid, 'with mpa_id', mpa.mpa_id)
            diff = {}
            diff_nogeom = {}
            if not created:
                diff = diffMpaWdpa(mpa, wpoly, poly)
            if diff:
                diffcount += 1
                mpadiffcount += 1
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
                    if mpadiffcount > 1:
                        geolog.write(',')
                    geolog.write('\n    "%s": ' % mpa.mpa_id)
                    json.dump(diff, geolog, indent=4, ensure_ascii=False)
                    geolog.flush()
                print('    PID:', wpoly.wdpa_pid, 'has %s field diffs %s' % (len(diff['mpa']), geominfo) )
                if logfile:
                    if mpadiffcount > 1:
                        log.write(',')
                    log.write('\n    "%s": ' % mpa.mpa_id)
                    json.dump(diff_nogeom, log, indent=4, ensure_ascii=False)
                    log.flush()

            # update record and create a revision so we can roll back if needed
            if not dryrun:
                with transaction.atomic(), reversion.create_revision():
                    updateMpaFromWdpaSmart(wpoly, mpa, poly, created, dryrun)
                    comment = 'Updated record from WDPA December 2020'
                    reference = 'World Database on Protected Areas, December 2020'
                    reversion.set_comment(comment)
                    User = get_user_model()
                    user = User.objects.get(username='russmo')
                    reversion.set_user(user)
                    reversion.add_meta(VersionMetadata, comment=comment, reference=reference)
            else:
                # do smart save dry run without saving and without transactions and revisions
                updateMpaFromWdpaSmart(wpoly, mpa, poly, created, dryrun)
        if logfile:
            log.write('\n}')
        if geologfile:
            geolog.write('\n}')
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
    mpa.marine = int(wpoly.marine)
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

    mpa.pa_def = str(wpoly.pa_def).lower() in ('1', 'yes', 'true', 't')
    mpa.own_type = wpoly.own_type
    mpa.verify_wdpa = wpoly.verif
    mpa.wdpa_metadataid = wpoly.metadataid

    if wpoly.marine == 0:
        if mpa.verification_state not in ('Internally Verified', 'Externally Verified'):
            # Keep original MPAtlas is_mpa value if verified,
            # otherwise set to is_mpa=False
            mpa.is_mpa = False;
            mpa.notes = mpa.notes + '\nSetting marine=0 and is_mpa=False because site is unverified.'

    if poly:
        newgeom = wpoly.geom.clone()
        # This buffer step takes forever on some sites, we handle making geoms valid elsewhere
        # try:
        #     newgeom = newgeom.buffer(0)
        # except:
        #     pass
        try:
            newgeom = geos.MultiPolygon(newgeom)
        except:
            pass
        mpa.geom = newgeom

    else:
        mpa.point_geom = wpoly.geom
    
    mpa.save()
    # mpa_post_save(sender=Mpa, instance=mpa)

def updateMpaFromWdpaSmart(wdpa, mpa, poly=True, created=False, dryrun=False):
    resolution = 1e-09
    mpa.is_point = False
    if not poly:
        mpa.is_point = True
        if mpa.geom:
            # existing mpa has geom, so don't use this point
            mpa.is_point = False
    wdpa_changedfields = []
    mpa_changedfields = []
    mpa_changedfields_old = []
    mpadiff_old = {}
    m_area = 0
    w_area = 0
    wold_area = 0
    if not created:
        try:
            m_area_qs = Mpa.objects.filter(mpa_id=mpa.mpa_id).annotate(geog_area=Area( Func(F('geom'), function='geography', template='%(expressions)s::%(function)s') ))
            m_area = m_area_qs.values_list('geog_area', flat=True)[0].sq_m
        except:
            m_area = 0
        try:
            w_area_qs = WDPA_POLY_NEW.objects.filter(wdpa_pid=wdpa.wdpa_pid).annotate(geom_nodup=MakeValid(Func(F('geom'), resolution, function='ST_RemoveRepeatedPoints'))).annotate(geog_area=Area( Func(F('geom_nodup'), function='geography', template='%(expressions)s::%(function)s') ))
            w_area = w_area_qs.values_list('geog_area', flat=True)[0].sq_m
            wdpa.geom = w_area_qs[0].geom_nodup
        except:
            w_area=0
        mpadiff = diffMpaWdpa(mpa, wdpa, poly)
        try:
            # Remove reserved fields here
            mpa_changedfields = [x for x in mpadiff['mpa'].keys() if x not in WDPA_RESERVED_FIELDS]
        except:
            pass
        
        try:
            wdpaold = WDPA_POLY_OLD.objects.filter(wdpa_pid=wdpa.wdpa_pid).annotate(geom_nodup=MakeValid(Func(F('geom'), resolution, function='ST_RemoveRepeatedPoints'))).annotate(geog_area=Area( Func(F('geom_nodup'), function='geography', template='%(expressions)s::%(function)s') ))[0]
            # Apply same validity processing as MPAtlas polygons for comparison
            wdpaold.geom = wdpaold.geom_nodup
            wold_area = wdpaold.geog_area.sq_m
        except:
            try:
                wdpaold = WDPA_POINT_OLD.objects.get(wdpa_pid=wdpa.wdpa_pid)
            except:
                wdpaold = None
                print('    INFO: Older WDPA record not found')
        if wdpaold:
            wdpadiff = diffWdpa(wdpa, wdpaold)
            try:
                wdpa_changedfields = wdpadiff['wdpa_new'].keys()
            except:
                pass
            mpadiff_old = diffMpaWdpa(mpa, wdpaold, poly)
            try:
                # Remove reserved fields here, use Mpa field names, not WDPA
                mpa_changedfields_old = [x for x in mpadiff_old['mpa'].keys() if x not in [WDPA_FIELD_MAP_INVERSE[i] for i in WDPA_RESERVED_FIELDS]]
            except:
                pass
    else:
        #new mpa object
        pass
    for mf, wf in WDPA_FIELD_MAP.items():
        if mf not in mpa_changedfields_old:
            if mf == 'wdpa_id':
                setattr(mpa, mf, int(getattr(wdpa, wf)))
            elif mf == 'pa_def':
                setattr(mpa, mf, str(getattr(wdpa, wf)).lower() in ('1', 'yes', 'true', 't'))
            elif mf == 'wdpa_metadataid':
                setattr(mpa, mf, int(getattr(wdpa, wf)))
            elif mf == 'marine':
                setattr(mpa, mf, int(getattr(wdpa, wf)))
            elif mf == 'status_year':
                if getattr(wdpa, wf) is not None and getattr(wdpa, wf) > 0:
                    # Don't set status_year if it's blank
                    setattr(mpa, mf, getattr(wdpa, wf))
                elif getattr(mpa, mf) == 0:
                    setattr(mpa, mf, None)
                    # Set status_year to Null if it is zero and wdpa has no better value
                    # This keeps us from having zeros in here, prefer Null/None
            else:
                setattr(mpa, mf, getattr(wdpa, wf))
        else:
            # MPA has different values than old WDPA
            # Keep these values but change all others
            # to latest WDPA values
            if mf in WDPA_USE_IF_MPA_BLANK.keys():
                mval = getattr(mpa, mf)
                if mval is None or mval == '' or mval == 0 or mval in ("Not Reported", "Not Applicable"):
                    setattr(mpa, mf, getattr(wdpa, wf))
                    if mf in mpa_changedfields_old:
                        mpa_changedfields_old.remove(mf)
    if wdpa.pa_def == False:
        mpa.is_mpa = False
    if wdpa.marine == 0:
        if mpa.verification_state not in ('Internally Verified', 'Externally Verified'):
            # Keep original MPAtlas is_mpa value if verified,
            # otherwise set to is_mpa=False
            mpa.is_mpa = False;
            mpa.notes = mpa.notes + '\nSetting marine=0 and is_mpa=False because site is unverified.'

    if poly:
        keep_mpatlas_geom = True
        similarity_pct_old = 99.99
        similarity_pct_new = 99.99
        if (m_area > 0 and wold_area > 0):
            similarity_pct_old = abs((m_area - wold_area)/m_area)
        if (m_area > 0 and w_area > 0):
            similarity_pct_new = abs((m_area - w_area)/m_area)
        similarity_pct_min = min(similarity_pct_old, similarity_pct_new)
        if created:
            # new record, so use WDPA geom
            keep_mpatlas_geom = False
        else:
            # not created, mpatlas record found
            if (similarity_pct_min < 1e-06 or m_area == 0):
                # MPAtlas has different boundaries than WDPA,
                # BUT they are very close in area, so just use new WDPA boundary instead
                keep_mpatlas_geom = False
                if m_area == 0:
                    print('    MPAtlas orig geom area is zero, using WDPA boundaries')
                else:
                    print('    Geom areas similar (%s%%), using WDPA boundaries' % (similarity_pct_min*100))
                if 'geom' in mpa_changedfields_old:
                    mpa_changedfields_old.remove('geom')
        if keep_mpatlas_geom:
            # MPAtlas has different boundaries than old WDPA, with different area,
            # so keep existing MPAtlas boundaries and don't import new WDPA boundaries
            print('    Geom areas %s%% dissimilar, keeping existing MPAtlas boundaries' % (similarity_pct_min*100))
            if 'geom' not in mpa_changedfields_old:
                mpa_changedfields_old.append('geom')
        else:        
            newgeom = wdpa.geom.clone()
            try:
                newgeom = geos.MultiPolygon(newgeom)
            except:
                pass
            mpa.geom = newgeom

            # force use of WDPA geom calc and reported fields if we use WDPA geom
            for wf in WDPA_GEOM_CALC_FIELDS:
                mf = WDPA_FIELD_MAP_INVERSE[wf]
                setattr(mpa, mf, getattr(wdpa, wf))
                if mf in mpa_changedfields_old:
                    mpa_changedfields_old.remove(mf)
    else:
        mpa.point_geom = wdpa.geom
    
    print('    Retained old MPAtlas values for: %s' % ' '.join(mpa_changedfields_old))
    if not dryrun:
        mpa.save()
    # mpa_post_save(sender=Mpa, instance=mpa)


