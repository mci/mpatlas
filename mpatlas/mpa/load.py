import os, re, csv
from django.contrib.gis.utils import LayerMapping
from models import MpaCandidate, mpacandidate_mapping
from models import Mpa, Contact, CandidateInfo
from wdpa.models import WdpaPolygon, WdpaPoint
from usmpa.models import USMpaPolygon

from django.contrib.gis import geos, gdal

from django.db import connection, transaction

mpacandidate_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Potential_MPAs/Potential_MPAs.shp'))

def import_candidates():
    cfilename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Potential_MPAs/Candidate_MPAs_MPAtlas_20120523.csv'))
    cfile = open(cfilename, "rU")
    creader = csv.reader(cfile, csv.excel)
    line = -1
    for row in creader:
        line += 1
        if line == 0:
            continue
        name = row[1]
        lon = row[2]
        lat = row[3]
        
        print name
        
        mpa = Mpa.objects.get_or_create(name=name, status='Proposed')[0]
        mpa.status = 'Proposed'
        mpa.country = ''
        mpa.is_point = True
        try:
            lon = float(lon)
            lat = float(lat)
            point = geos.Point(lon, lat, srid=gdal.SpatialReference('WGS84').srid)
            mpa.point_geom = point
            mpa.point_geog = point
            mpa.point_geom_smerc = point.transform(3857)
            mpa.point_within = point
        except:
            pass
        mpa.save()
        
        candidate = CandidateInfo.objects.get_or_create(mpa=mpa)[0]
        
        candidate.source = row[4]
        candidate.scope = row[5]
        candidate.basin = row[6]
        candidate.region = row[7]
        candidate.location = row[8]
        candidate.eez_or_highseas = row[9]
        candidate.lead_organization = row[10]
        candidate.partner_organizations = row[11]
        candidate.key_agency_or_leader = row[12]
        candidate.timeframe = row[13]
        candidate.current_protection = row[14]
        candidate.desired_protection = row[15]
        candidate.importance = row[16]
        candidate.opportunity = row[17]
        candidate.reference1 = row[18]
        candidate.reference1 = row[19]
        
        candidate.save()

def run_mpacandidate(strict=True, verbose=True, **kwargs):
    lm_mpacandidate = LayerMapping(MpaCandidate, mpacandidate_shp, mpacandidate_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_mpacandidate.save(strict=strict, verbose=verbose, **kwargs)

def wdpapoly2mpa():
    wpolys = WdpaPolygon.objects.all().defer(*WdpaPolygon.get_geom_fields()).order_by('wdpaid')
    count = 0
    for wpoly in wpolys:
        mpa, created = Mpa.objects.get_or_create(wdpa_id=wpoly.wdpaid)
        count += 1
        print count
        mpa.name = wpoly.name
        mpa.wdpa_id = wpoly.wdpaid
        mpa.country = wpoly.country
        mpa.sub_location = wpoly.sub_loc
        mpa.designation = wpoly.desig
        mpa.designation_eng = wpoly.desig_eng
        mpa.designation_type = wpoly.desig_type
        mpa.iucn_category = wpoly.iucn_cat
        mpa.int_criteria = wpoly.int_crit
        mpa.marine = wpoly.marine
        mpa.status = wpoly.status
        mpa.status_year = wpoly.status_yr
        mpa.area_notes = wpoly.area_notes
        mpa.rep_m_area = wpoly.rep_m_area
        mpa.calc_m_area = wpoly.gis_m_area
        mpa.rep_area = wpoly.rep_area
        mpa.calc_area = wpoly.gis_area
        mpa.gov_type = wpoly.gov_type
        mpa.mgmt_auth = wpoly.mang_auth
        mpa.mgmt_plan_ref = wpoly.mang_plan
        
        #mpa.geom_smerc = wpoly.geom_smerc
        #mpa.geom = wpoly.geom
        #mpa.geog = wpoly.geog
        
        mpa.save()
    
    # SQL update all geometry rows, much faster than through django
    print 'UPDATE geometry columns'
    cursor = connection.cursor()
    cursor.execute("UPDATE mpa_mpa SET geog = w.geog FROM wdpa_wdpapolygon as w WHERE mpa_mpa.wdpa_id = w.wdpaid")
    transaction.commit_unless_managed()
    print 'UPDATE complete'
    
    Mpa.set_all_geom_from_geog()

def wdpapoint2mpa():
    wpoints = WdpaPoint.objects.all().order_by('wdpaid')
    count = 0
    for wpoint in wpoints:
        try:
            mpa, created = Mpa.objects.get_or_create(wdpa_id=wpoint.wdpaid)
        except:
            mpa = Mpa() # create a new object if wpoint has no wdpaid
            print 'wdpaid error', wpoint.wdpaid, wpoint.pk
        count += 1
        print count
        mpa.is_point = True
        mpa.name = wpoint.name
        mpa.wdpa_id = wpoint.wdpaid
        mpa.country = wpoint.country
        mpa.sub_location = wpoint.sub_loc
        mpa.designation = wpoint.desig
        mpa.designation_eng = wpoint.desig_eng
        mpa.designation_type = wpoint.desig_type
        mpa.iucn_category = wpoint.iucn_cat
        mpa.int_criteria = wpoint.int_crit
        mpa.marine = wpoint.marine
        mpa.status = wpoint.status
        mpa.status_year = wpoint.status_yr
        mpa.rep_m_area = wpoint.rep_m_area
        mpa.rep_area = wpoint.rep_area
        mpa.gov_type = wpoint.gov_type
        mpa.mgmt_auth = wpoint.mang_auth
        mpa.mgmt_plan_ref = wpoint.mang_plan

        #mpa.point_geom_smerc = wpoint.point_geom_smerc
        #mpa.point_geom = wpoint.point_geom
        #mpa.point_geog = wpoint.point_geog

        mpa.save()

    # SQL update all geometry rows, much faster than through django
    print 'UPDATE point geometry columns'
    cursor = connection.cursor()
    cursor.execute("UPDATE mpa_mpa SET point_geog = w.geog FROM wdpa_wdpapoint as w WHERE mpa_mpa.wdpa_id = w.wdpaid")
    transaction.commit_unless_managed()
    print 'UPDATE complete'
    
    Mpa.set_all_geom_from_geog()

def usmpa2mpa(usmpa_id=None):
    usmpas = USMpaPolygon.objects.all().defer(*USMpaPolygon.get_geom_fields()).order_by('site_id')
    if usmpa_id is not None:
        usmpas = usmpas.filter(site_id=usmpa_id)
    count = 0
    for usmpa in usmpas:
        mpa, created = Mpa.objects.get_or_create(usmpa_id=usmpa.site_id)
        count += 1
        print count, usmpa.site_name, usmpa.state, usmpa.site_id
        mpa.name = usmpa.site_name
        mpa.long_name = usmpa.site_name
        mpa.short_name = usmpa.site_label
        mpa.usmpa_id = usmpa.site_id
        mpa.country = 'USA'
        
        mpa.mgmt_auth = usmpa.mgmt_agency
        if usmpa.mgmt_plan and usmpa.mgmt_plan.lower() != 'no management plan':
            mpa.mgmt_plan_type = usmpa.mgmt_plan
        mpa.mgmt_plan_ref = None
        mpa.gov_type = usmpa.gov_level
        
        statecode = re.compile(r'^(\D\D)\d*')
        match = statecode.match(usmpa.site_id)
        if match:
            mpa.sub_location = match.group(1)
            print '  ', mpa.sub_location
        
        mpa.constancy = usmpa.constancy
        if usmpa.permanence == 'Permanent':
            mpa.permanence = 'Permanent'
        elif usmpa.permanence == 'Conditional':
            mpa.permanence = 'Non-Permanent - Conditional'
        elif usmpa.permanence == 'Temporary':
            mpa.permanence = 'Non-Permanent - Temporary'
        
        #mpa.designation = usmpa.desig
        #mpa.designation_eng = usmpa.desig_eng
        mpa.designation_type = 'National'
        mpa.marine = True
        mpa.status = 'Designated'
        
        if (usmpa.establishment_year):
            mpa.status_year = int(usmpa.establishment_year)
        
        #mpa.protection_level
        
        if usmpa.primary_conservation_focus == 'Natural Heritage':
            mpa.primary_conservation_focus == 'Biodiversity Protection'
        elif usmpa.primary_conservation_focus == 'Sustainable Production':
            mpa.primary_conservation_focus == 'Biomass Enhancement'
        elif usmpa.primary_conservation_focus == 'Cultural Heritage':
            mpa.primary_conservation_focus == 'Cultural Heritage'
        else:
            mpa.primary_conservation_focus == 'Unknown'
        
        confoci = usmpa.conservation_focus.split(' and ')
        for i in range(0,len(confoci)):
            confocus = confoci[i]
            if confocus == 'Natural Heritage':
                confocus == 'Biodiversity Protection'
            elif confocus == 'Sustainable Production':
                confocus == 'Biomass Enhancement'
            elif confocus == 'Cultural Heritage':
                confocus == 'Cultural Heritage'
            else:
                confocus == 'Unknown'
            if i==0:
                mpa.secondary_conservation_focus = confocus
            else:
                tertiary_conservation_focus = confocus
        
        if usmpa.protection_focus == 'Ecosystem':
            mpa.protection_focus = 'Ecosystem'
        elif usmpa.protection_focus == 'Focal Resource':
            mpa.protection_focus = 'Focal Species'
        
        if usmpa.fishing_restriction == 'No Site Restrictions':
            mpa.fishing = 'Yes'
        elif usmpa.fishing_restriction == 'Commercial and Recreational Fishing Prohibited':
            mpa.fishing = 'No'
        elif usmpa.fishing_restriction == 'Restrictions Unknown':
            mpa.fishing = 'Unknown'
        else:
            mpa.fishing = 'Some Restrictions'
        mpa.fishing_info = usmpa.fishing_restriction
        
        if usmpa.vessel == 'Prohibited':
            mpa.access = 'No'
        elif usmpa.vessel == 'Restricted':
            mpa.access = 'Restricted'
        elif usmpa.vessel == 'Unrestricted':
            mpa.access = 'Yes'
        
        # Create a contact and url for this site
        c, created = Contact.objects.get_or_create(agency=usmpa.site_label + ' Website', url=usmpa.url)
        #c.mpa_main_set.add(mpa)
        mpa.contact = c
        
        #mpa.geom_smerc = wpoly.geom_smerc
        #mpa.geom = wpoly.geom
        #mpa.geog = wpoly.geog

        mpa.save()

    # SQL update all geometry rows, much faster than through django
    print 'UPDATE geometry columns'
    cursor = connection.cursor()
    cursor.execute("UPDATE mpa_mpa SET geom = u.geom, geog = u.geog, geom_smerc = u.geom_smerc FROM usmpa_usmpapolygon as u WHERE mpa_mpa.usmpa_id = u.site_id")
    transaction.commit_unless_managed()
    print 'UPDATE complete'
    
    Mpa.set_all_geom_from_geog()
