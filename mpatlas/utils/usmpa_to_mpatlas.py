from mpa.models import Mpa
from django.contrib.gis import geos, gdal
import json

usmpa_file = '/home/mpatlas/usmpa_2014_CA.geojson'
cdfw_file = '/home/mpatlas/MPA_CA_Existing_2015.geojson'

create_ids =[
    u'CA275', u'CA320', u'CA283', u'CA280', u'CA296', u'CA321', u'CA284', u'CA297', u'CA308', u'CA322', u'CA309', u'CA294', u'CA315', u'CA314', u'CA317', u'CA316', u'CA269', u'CA268', u'CA313', u'CA312', u'CA265', u'CA326', u'CA267', u'CA266', u'CA319', u'CA318', u'CA289', u'CA288', u'CA286', u'CA299', u'CA295', u'CA282', u'CA323', u'CA287', u'CA291', u'CA327', u'CA292', u'CA285', u'CA281', u'CA293', u'CA311', u'CA310', u'CA306', u'CA307', u'CA304', u'CA305', u'CA302', u'CA303', u'CA300', u'CA301', u'CA276', u'CA277', u'CA274', u'CA279', u'CA272', u'CA273', u'CA270', u'CA271', u'CA324', u'CA328', u'CA325', u'CA290', u'CA298', u'CA278'
]
update_ids = [
    u'CA28', u'CA29', u'CA22', u'CA23', u'CA20', u'CA21', u'CA26', u'CA27', u'CA24', u'CA25', u'CA264', u'CA261', u'CA260', u'CA262', u'CA229', u'CA141', u'CA249', u'CA248', u'CA243', u'CA242', u'CA241', u'CA240', u'CA247', u'CA246', u'CA245', u'CA244', u'CA34', u'CA31', u'CA30', u'CA33', u'CA32', u'CA38', u'CA254', u'CA255', u'CA256', u'CA257', u'CA250', u'CA251', u'CA252', u'CA253', u'CA258', u'CA259', u'CA150', u'CA40', u'CA45', u'CA48', u'CA221', u'CA220', u'CA223', u'CA222', u'CA225', u'CA224', u'CA227', u'CA226', u'CA140', u'CA228', u'CA142', u'CA143', u'CA144', u'CA145', u'CA146', u'CA147', u'CA53', u'CA52', u'CA54', u'CA233', u'CA151', u'CA231', u'CA236', u'CA237', u'CA234', u'CA235', u'CA238', u'CA239', u'CA139', u'CA138', u'CA137', u'CA136', u'CA113', u'CA6', u'CA209', u'CA208', u'CA207', u'CA206', u'CA205', u'CA204', u'CA203', u'CA202', u'CA201', u'CA19', u'CA18', u'CA17', u'CA16', u'CA15', u'CA14', u'CA13', u'CA12', u'CA11', u'CA10', u'CA218', u'CA219', u'CA94', u'CA210', u'CA211', u'CA212', u'CA213', u'CA214', u'CA215', u'CA216', u'CA217', u'CA9', u'CA8', u'CA3', u'CA2', u'CA1', u'CA7', u'CA116', u'CA5', u'CA4'
]
remove_ids = [
    u'CA82', u'CA90', u'CA148', u'CA105', u'CA106', u'CA107', u'CA100', u'CA81', u'CA102', u'CA83', u'CA51', u'CA78', u'CA37', u'CA50', u'CA56', u'CA55', u'CA71', u'CA73', u'CA75', u'CA74', u'CA76', u'CA80', u'CA84', u'CA93', u'CA92', u'CA49', u'CA152', u'CA98', u'CA104', u'CA85', u'CA135', u'CA41', u'CA42', u'CA43', u'CA66', u'CA67', u'CA60', u'CA263', u'CA230'
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
            print m.usmpa_id, m.pk

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
                m.access_info += '\nVessels prohibited.'
            elif p['Vessel'] == 'Restricted':
                m.access = 'Restricted'
                m.access_info += '\nVessels restricted.'
            if p['Anchor'] in ('Prohibited', 'Restricted'):
                m.access_info += '\nAnchoring %s' % (p['Anchor'].lower())

            if p['Fish_Rstr'] == 'Commercial and Recreational Fishing Prohibited':
                m.fishing = 'No'
            elif p['Fish_Rstr'] == 'No site Restrictions':
                m.fishing = 'Yes'
            else:
                m.fishing = 'Some Restrictions'
            m.fishing_info += '\n%s' % (p['Fish_Rstr'])

            m.status = 'Designated'

            m.notes += '\nUS National System status: %s' % (p['NS_Full'])
            m.notes += '\nURL: %s' % (p['URL'])

            m.country = 'USA'
            m.sublocation = 'US-CA'

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


def update_cdfw():
    with open(cdfw_file) as f:
        j=json.load(f)
        for f in j['features']:
            if f['properties']['USMPA_ID']:
                p = f['properties']
                m = Mpa.objects.get(usmpa_id=p['USMPA_ID'])
                print m.usmpa_id, m.pk
                gj = f['geometry']
                gjj = json.dumps(gj)
                geom = geos.GEOSGeometry(gjj)
                if geom.geom_type == 'Polygon':
                    geom = geos.MultiPolygon(geom)
                m.geom = geom
                m.name = p['FULLNAME']
                m.short_name = p['NAME']
                m.save()
