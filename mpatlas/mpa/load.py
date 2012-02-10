import os
from django.contrib.gis.utils import LayerMapping
from models import MpaCandidate, mpacandidate_mapping
from models import Mpa
from wdpa.models import WdpaPolygon, WdpaPoint

mpacandidate_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Potential_MPAs/Potential_MPAs.shp'))

def run_mpacandidate(strict=True, verbose=True, **kwargs):
    lm_mpacandidate = LayerMapping(MpaCandidate, mpacandidate_shp, mpacandidate_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_mpacandidate.save(strict=strict, verbose=verbose, **kwargs)

def wdpapoly2mpa():
    wpolys = WdpaPolygon.objects.all().defer(*WdpaPolygon.get_geom_fields())
    for wpoly in wpolys:
        mpa = Mpa()
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
        mpa.mgmt_plan = wpoly.mang_plan
        mpa.save()
