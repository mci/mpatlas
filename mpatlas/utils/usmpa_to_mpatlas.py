from __future__ import unicode_literals
from __future__ import print_function
from mpa.models import Mpa
from django.contrib.gis import geos, gdal
import json

usmpa_file = '/home/mpatlas/usmpa_2014_CA.geojson'
cdfw_file = '/home/mpatlas/MPA_CA_Existing_2015.geojson'

create_ids =[
    'CA275', 'CA320', 'CA283', 'CA280', 'CA296', 'CA321', 'CA284', 'CA297', 'CA308', 'CA322', 'CA309', 'CA294', 'CA315', 'CA314', 'CA317', 'CA316', 'CA269', 'CA268', 'CA313', 'CA312', 'CA265', 'CA326', 'CA267', 'CA266', 'CA319', 'CA318', 'CA289', 'CA288', 'CA286', 'CA299', 'CA295', 'CA282', 'CA323', 'CA287', 'CA291', 'CA327', 'CA292', 'CA285', 'CA281', 'CA293', 'CA311', 'CA310', 'CA306', 'CA307', 'CA304', 'CA305', 'CA302', 'CA303', 'CA300', 'CA301', 'CA276', 'CA277', 'CA274', 'CA279', 'CA272', 'CA273', 'CA270', 'CA271', 'CA324', 'CA328', 'CA325', 'CA290', 'CA298', 'CA278'
]
update_ids = [
    'CA28', 'CA29', 'CA22', 'CA23', 'CA20', 'CA21', 'CA26', 'CA27', 'CA24', 'CA25', 'CA264', 'CA261', 'CA260', 'CA262', 'CA229', 'CA141', 'CA249', 'CA248', 'CA243', 'CA242', 'CA241', 'CA240', 'CA247', 'CA246', 'CA245', 'CA244', 'CA34', 'CA31', 'CA30', 'CA33', 'CA32', 'CA38', 'CA254', 'CA255', 'CA256', 'CA257', 'CA250', 'CA251', 'CA252', 'CA253', 'CA258', 'CA259', 'CA150', 'CA40', 'CA45', 'CA48', 'CA221', 'CA220', 'CA223', 'CA222', 'CA225', 'CA224', 'CA227', 'CA226', 'CA140', 'CA228', 'CA142', 'CA143', 'CA144', 'CA145', 'CA146', 'CA147', 'CA53', 'CA52', 'CA54', 'CA233', 'CA151', 'CA231', 'CA236', 'CA237', 'CA234', 'CA235', 'CA238', 'CA239', 'CA139', 'CA138', 'CA137', 'CA136', 'CA113', 'CA6', 'CA209', 'CA208', 'CA207', 'CA206', 'CA205', 'CA204', 'CA203', 'CA202', 'CA201', 'CA19', 'CA18', 'CA17', 'CA16', 'CA15', 'CA14', 'CA13', 'CA12', 'CA11', 'CA10', 'CA218', 'CA219', 'CA94', 'CA210', 'CA211', 'CA212', 'CA213', 'CA214', 'CA215', 'CA216', 'CA217', 'CA9', 'CA8', 'CA3', 'CA2', 'CA1', 'CA7', 'CA116', 'CA5', 'CA4'
]
remove_ids = [
    'CA82', 'CA90', 'CA148', 'CA105', 'CA106', 'CA107', 'CA100', 'CA81', 'CA102', 'CA83', 'CA51', 'CA78', 'CA37', 'CA50', 'CA56', 'CA55', 'CA71', 'CA73', 'CA75', 'CA74', 'CA76', 'CA80', 'CA84', 'CA93', 'CA92', 'CA49', 'CA152', 'CA98', 'CA104', 'CA85', 'CA135', 'CA41', 'CA42', 'CA43', 'CA66', 'CA67', 'CA60', 'CA263', 'CA230'
]

fieldmap = {
    'usmpa_id' : 'Site_ID',
    'rep_area' : 'Area_KM_Total',
    'name' : 'Site_Name',
    'short_name' : 'Site_Label',
    'gov_type' : 'Gov_Level',
    'mgmt_plan_type' : 'Mgmt_Plan',
    'mgmt_auth' : 'Mgmt_Agen',
    'primary_conservation_focus' : 'Pri_Con_Foc',
    'protection_focus' : 'Prot_Focus',
    'permanence' : 'Permanence',
    'constancy' : 'Constancy',
    'status_year' : 'Estab_Yr',
}

def update_usmpa():
    with open(usmpa_file) as f:
        j=json.load(f)
        for usmpa in j['features']:
            p = usmpa['properties']
            g = usmpa['geometry']

            m = Mpa.objects.get(usmpa_id=p['Site_ID'])
            print(m.usmpa_id, m.pk)

            for key,value in fieldmap.items():
                setattr(m, key, p[value])

            if p['Prot_Lvl'] in ('No Take', 'No Access', 'No Impact'):
                m.no_take = 'All'
            elif p['Prot_Lvl'] in ('Zoned w/No Take Areas'):
                m.no_take = 'Part'
            else:
                m.no_take = 'None'

            foci = p['Cons_Focus'].split(' and ')
            fnum = 0
            for focus in foci:
                fnum += 1
                if focus == p['Pri_Con_Foc']:
                    continue
                if fnum == 1:
                    m.secondary_conservation_focus = focus
                else:
                    m.tertiary_conservation_focus = focus

            if p['Prot_Lvl'] in ('No Access', 'No Impact'):
                m.access = 'No'
            elif p['Vessel'] == 'Prohibited':
                m.access = 'Restricted'
                if m.access_info is None:
                    m.access_info = ''
                m.access_info += '\nVessels prohibited.'
            elif p['Vessel'] == 'Restricted':
                m.access = 'Restricted'
                if m.access_info is None:
                    m.access_info = ''
                m.access_info += '\nVessels restricted.'
            if p['Anchor'] in ('Prohibited', 'Restricted'):
                if m.access_info is None:
                    m.access_info = ''
                m.access_info += '\nAnchoring %s' % (p['Anchor'].lower())

            if p['Fish_Rstr'] == 'Commercial and Recreational Fishing Prohibited':
                m.fishing = 'No'
            elif p['Fish_Rstr'] == 'No site Restrictions':
                m.fishing = 'Yes'
            else:
                m.fishing = 'Some Restrictions'
            if m.fishing_info is None:
                m.fishing_info = ''
            m.fishing_info += '\n%s' % (p['Fish_Rstr'])

            m.status = 'Designated'

            if m.notes is None:
                m.notes = ''
            m.notes += '\nUS National System status: %s' % (p['NS_Full'])
            m.notes += '\nURL: %s' % (p['URL'])

            m.country = 'USA'
            m.sub_location = 'US-CA'

            gj = g
            gjj = json.dumps(gj)
            geom = geos.GEOSGeometry(gjj)
            if geom.geom_type == 'Polygon':
                geom = geos.MultiPolygon(geom)
            m.geom = geom

            m.save()
    for usmpa_id in remove_ids:
        m = Mpa.objects.get(usmpa_id=usmpa_id)
        m.verification_state = 'Rejected as MPA'
        m.verification_reason += '\nRemoved from US MPA Center inventory'
        m.save()


def update_cdfw():
    with open(cdfw_file) as f:
        j=json.load(f)
        for f in j['features']:
            if f['properties']['USMPA_ID']:
                p = f['properties']
                m = Mpa.objects.get(usmpa_id=p['USMPA_ID'])
                print(m.usmpa_id, m.pk)
                gj = f['geometry']
                gjj = json.dumps(gj)
                geom = geos.GEOSGeometry(gjj)
                if geom.geom_type == 'Polygon':
                    geom = geos.MultiPolygon(geom)
                m.geom = geom
                m.name = p['FULLNAME']
                m.short_name = p['NAME']
                m.save()
