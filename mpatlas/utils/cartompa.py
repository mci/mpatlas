from __future__ import unicode_literals
from __future__ import print_function
import sys, json, time
#from cartodb import CartoDBAPIKey, CartoDBException
from carto.auth import APIKeyAuthClient
from carto.sql import SQLClient, CartoException
from mpa.models import Mpa
from campaign.models import Campaign
from django.db import connections, connection
from psycopg2.extensions import adapt, AsIs
from django.contrib.gis import geos
from django.conf import settings

# get psycopg2 connection object, we need it to force psycopg2.extensions.adapt
# function to encode strings to utf-8. It defaults to latin-1 if no connection
# is present, which is not helpful. Here we use the low level connection used
# by django.
try:
    djangoconn = connections['default']
except:
    djangoconn = connection
conn = djangoconn.cursor().connection

# API key should be defined in local_settings.py
API_KEY = getattr(settings, "CARTO_API_KEY", '1234')
carto_domain = 'mpatlas'

USERNAME="mpatlas"
USR_BASE_URL = "https://{user}.carto.com/".format(user=USERNAME)

# Simplification settings for large/complex geometries
SIMPLE_THRESHOLD = getattr(settings, "CARTO_SIMPLE_THRESHOLD", 100000)
SIMPLE_TOLERANCE = getattr(settings, "CARTO_SIMPLE_TOLERANCE", 0.0001)

# fields variable is overwritten at end of module, listing all fields needed to pull from mpatlas
# via a .values(*fields) call.  Update this for new columns.
fields = []

# default queryset to use for syncing from mpatlas to Carto
mpas = Mpa.objects.exclude(verification_state='Rejected as MPA').exclude(geom__isnull=True).order_by('-mpa_id').only('mpa_id')

def hex_or_none(geom):
    try:
        return geom.hexewkb
    except:
        return None

def adaptParam(p):
    '''Convert and escape python objects for use in Postgresql SQL statements.
       Uses the psycopg2.extensions.adapt function rather than using param
       substitution at the database cursor level or other Django internals.
       This should provide reasonable SQL injection protection with the
       flexibility to generate and send Carto SQL statements via http.

       We are hoping that we have passed in a unicode string to adapt()
       Passing in a byte string (str on python2, byte on python3) will cause
       adapt() to cast string as ::bytea.
       WARNING: adapt() always returns a byte string. Formatting and inserting
       byte string variables into 'unicode string %s' % (b'adapted')
       results in "unicode string b'adapted'" which is not what we want in
       SQL statements
    '''
    if isinstance(p, geos.GEOSGeometry):
        p = p.wkt
    a = p
    try:
        # try a coercion through utf-8 byte.decode -> unicode string
        p = type(b'').decode(p, 'utf-8')
    except:
        try:
            # try a coercion through unicode.encode -> utf-8 byte string -> unicode string
            p = type('').encode(p, 'utf-8').decode('utf-8')
        except:
            pass
    try:
        a = adapt(p)
        try:
            a.prepare(conn)
        except:
            pass
        a = a.getquoted()
    except UnicodeEncodeError:
        try:
            a = adapt(type('').encode(json.loads(json.dumps(p)), 'utf-8'))
            try:
                a.prepare(conn)
            except:
                pass
            a = a.getquoted()
        except:
            pass
    if type(a) is type(b''):
        # bring utf-8 byte string back to unicode type (str in python3)
        try:
            a = a.decode('utf-8')
        except:
            pass
    return a

def updateMpaSQL(m, simple_threshold=SIMPLE_THRESHOLD, simple_tolerance=SIMPLE_TOLERANCE):
    '''Returns a Postgresql SQL statement that will update or insert an Mpa record
       from the MPAtlas database into the mpatlas table on Carto.  The Carto
       mpatlas table columns are not a one-to-one match with mpa_mpa columns.
    '''
    if not isinstance(m, Mpa):
        m = Mpa.objects.get(pk=m)
    try:
        mpadict = Mpa.objects.filter(pk=m.mpa_id).values(*fields).first()
        mpadict['categories'] = '{' + ', '.join(m.categories.names()) + '}'
        lookup = {'mpa_id': m.mpa_id, 'geom': adaptParam(m.geom.hexewkb), 'columns': ', '.join(mpadict.keys()), 'values': ', '.join([adaptParam(v) for v in mpadict.values()])}
        if simple_threshold > 0 and m.geom.num_coords >= simple_threshold:
            # lookup['geom'] = adaptParam(m.simple_geom.hexewkb)
            lookup['geom'] = adaptParam(m.geom.simplify(simple_tolerance).hexewkb)
        upsert = '''
            UPDATE mpatlas SET (the_geom, %(columns)s) = (%(geom)s::geometry, %(values)s) WHERE mpa_id=%(mpa_id)s;
                INSERT INTO mpatlas (the_geom, %(columns)s)
                    SELECT %(geom)s::geometry, %(values)s
                    WHERE NOT EXISTS (SELECT 1 FROM mpatlas WHERE mpa_id=%(mpa_id)s);
        ''' % (lookup)
        return upsert
    except Exception as e:
        print('ERROR processing mpa %s: ' % m.mpa_id, e)
        raise(e)

def updateMpa(m, simple_threshold=SIMPLE_THRESHOLD, simple_tolerance=SIMPLE_TOLERANCE):
    '''Executes Mpa update/insert statements using the Carto API via the carto module.
       Returns mpa.mpa_id or None if error'''
    if not isinstance(m, Mpa):
        m = Mpa.objects.get(pk=m)
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    try:
        sql.send(updateMpaSQL(m, simple_threshold=simple_threshold, simple_tolerance=simple_tolerance))
        return m.pk
    except CartoException as e:
        print('Carto Error for mpa_id %s:' % m.pk, e)
    return None

def updateAllMpas(mpas=mpas, simple_threshold=0, simple_tolerance=0.0001, step=10, limit=None):
    '''Execute bulk Mpa update/insert statements using the Carto API via the carto module.
       mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
       simple_threshold = number of vertices a feature must contain in order to send
           simplified geometry to Carto to save disk space.
           [0 = never send simplified geometries, 1 = always send simplified geometries]
       simple_tolerance = Douglas-Peucker simplification tolerance
       step = number of Mpas to update per http transaction
       limit = only process a subset of records, useful for testing
       Returns list of mpa.mpa_ids that were not processed due to errors, empty list if no errors
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    nummpas = mpas.count()
    if limit:
        nummpas = min(limit, nummpas)
    print('Processing %s of %s mpa records at a time' % (step, nummpas))
    r = list(range(0,nummpas+2,step))
    if r and r[-1] < nummpas:
        r.append(nummpas)
    error_ids = []
    start = time.time()
    for i in range(0,len(r)-1):
        r0 = r[i]
        r1 = r[i+1]
        print('Records [%s - %s]' % (r0, r1-1))
        step_ids = []
        upsert = ''
        for m in mpas[r0:r1]:
            try:
                upsert += updateMpaSQL(m, simple_threshold=simple_threshold, simple_tolerance=simple_tolerance)
                step_ids.append(m.pk)
            except:
                error_ids.append(m.pk)
                print('Skipping Mpa', m.pk)
        # Now update this batch of records in Carto
        try:
            sql.send(upsert)
        except CartoException as e:
            print('Carto Error for mpa_ids %s:' % step_ids, e)
            print('Trying single updates.')
            for mpa_id in step_ids:
                try:
                    success = updateMpa(mpa_id, simple_threshold=simple_threshold, simple_tolerance=simple_tolerance)
                    if not success:
                        raise CartoException
                except CartoException as e:
                    error_ids.append(mpa_id)
                    print('Carto Error for mpa_id %s:' % mpa_id, e)
    end = time.time()
    print('TOTAL', end - start, 'sec elapsed')
    return error_ids

def removeCartoMpas(mpas=mpas, dryrun=False):
    '''Execute Mpa remove statements using the Carto API via the carto module.
       mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
       dryrun = [False] if true, just return list of mpa_ids to be removed but don't run SQL.
       Returns list of mpa.mpa_ids that were removed, empty list if none removed.
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    nummpas = mpas.count()
    local_ids = mpas.values_list('mpa_id', flat=True)
    if local_ids:
        deletesql = '''
            DELETE FROM mpatlas WHERE mpa_id IN %(local_ids)s;
        ''' % ({'local_ids': adaptParam(tuple(local_ids))})
        if not dryrun:
            try:
                sql.send(deletesql)
            except CartoException as e:
                print('Carto Error deleting %s mpas:' % len(local_ids), e)
    return local_ids

def purgeCartoMpas(mpas=mpas, dryrun=False):
    '''Execute Mpa remove statements using the Carto API via the carto module for
       mpas in the Carto mpatlas table that are not found in the passed mpas queryset.
       mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
       dryrun = [False] if true, just return list of mpa_ids to be purged but don't run SQL.
       Returns list of mpa.mpa_ids that were removed, empty list if none removed.
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    nummpas = mpas.count()
    local_ids = mpas.values_list('mpa_id', flat=True)
    carto_idsql = '''
        SELECT mpa_id FROM mpatlas ORDER BY mpa_id;
    '''
    try:
        result = sql.send(carto_idsql)
    except CartoException as e:
        print('Carto Error for getting mpa_ids', e)
    carto_ids = [i['mpa_id'] for i in result['rows']]
    missing = list(set(carto_ids) - set(local_ids))
    missing.sort()
    if missing:
        deletesql = '''
            DELETE FROM mpatlas WHERE mpa_id IN %(missing)s;
        ''' % ({'missing': adaptParam(tuple(missing))})
        if not dryrun:
            try:
                sql.send(deletesql)
            except CartoException as e:
                print('Carto Error deleting %s mpas:' % len(missing), e)
    return missing

def truncateCartoMpas(dryrun=False):
    '''Execute truncate statements using the Carto API via the carto module for
       to clear out all records in table.
       dryrun = [False] if true, just number of records to be purged but don't run SQL.
       Returns list of mpa.mpa_ids that were removed, empty list if none removed.
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    nummpas = mpas.count()
    local_ids = mpas.values_list('mpa_id', flat=True)
    carto_idsql = '''
        SELECT mpa_id FROM mpatlas ORDER BY mpa_id;
    '''
    try:
        result = sql.send(carto_idsql)
    except CartoException as e:
        print('Carto Error for getting mpa_ids', e)
    carto_ids = [i['mpa_id'] for i in result['rows']]
    truncatesql = '''
        TRUNCATE TABLE mpatlas;
    '''
    if not dryrun:
        try:
            sql.send(truncatesql)
        except CartoException as e:
            print('Carto Error truncating %s mpas:' % len(carto_ids), e)
    return carto_ids

def addMissingMpas(mpas=mpas, simple_threshold=SIMPLE_THRESHOLD, simple_tolerance=SIMPLE_TOLERANCE, dryrun=False):
    '''Execute Mpa remove statements using the Carto API via the carto module for
       mpas in the Carto mpatlas table that are not found in the passed mpas queryset.
       mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
       dryrun = [False] if true, just return list of mpa_ids to be purged but don't run SQL.
       Returns list of mpa.mpa_ids that were removed, empty list if none removed.
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    nummpas = mpas.count()
    local_ids = mpas.values_list('mpa_id', flat=True)
    carto_idsql = '''
        SELECT mpa_id FROM mpatlas ORDER BY mpa_id;
    '''
    try:
        result = sql.send(carto_idsql)
    except CartoException as e:
        print('Carto Error for getting mpa_ids', e)
    carto_ids = [i['mpa_id'] for i in result['rows']]
    missing = list(set(local_ids) - set(carto_ids))
    missing.sort()
    if missing:
        addmpas = mpas.filter(mpa_id__in = missing)
        if not dryrun:
            updateAllMpas(addmpas, simple_threshold=simple_threshold, simple_tolerance=simple_tolerance)
    return missing

fields = [
    'mpa_id',
    # 'geom',
    'name',
    'designation',
    'designation_eng',
    'designation_type',
    'access',
    'access_citation',
    'access_info',
    'calc_area',
    'calc_m_area',
    # 'categories',
    'conservation_effectiveness',
    'conservation_focus_citation',
    'conservation_focus_info',
    'constancy',
    'constancy_citation',
    'contact_id',
    'country',
    'fishing',
    'fishing_citation',
    'fishing_info',
    'gov_type',
    'implementation_date',
    'implemented',
    'int_criteria',
    'is_mpa',
    'is_point',
    'iucn_category',
    'long_name',
    'marine',
    'mgmt_auth',
    'mgmt_plan_ref',
    'mgmt_plan_type',
    'no_take',
    'no_take_area',
    'notes',
    'other_ids',
    'permanence',
    'permanence_citation',
    'primary_conservation_focus',
    'secondary_conservation_focus',
    'tertiary_conservation_focus',
    'protection_focus',
    'protection_focus_citation',
    'protection_focus_info',
    'protection_level',
    'rep_area',
    'rep_m_area',
    'short_name',
    'slug',
    'sovereign',
    'status',
    'status_year',
    'sub_location',
    'summary',
    'usmpa_id',
    'verification_reason',
    'verification_state',
    'verified_by',
    'verified_date',
    'wdpa_id',
    'wdpa_notes'
]

remote_fields = fields + ['categories']


# default queryset to use for syncing from mpatlas to Carto
campaigns = Campaign.objects.order_by('-id').only('id')

# fields variable is overwritten at end of module, listing all fields needed to pull from mpatlas
# via a .values(*fields) call.  Update this for new columns.
campaign_fields = []

def updateCampaignSQL(c):
    '''Returns a Postgresql SQL statement that will update or insert an Mpa record
       from the MPAtlas database into the mpatlas table on Carto.  The Carto
       mpatlas table columns are not a one-to-one match with mpa_mpa columns.
    '''
    if not isinstance(c, Campaign):
        c = Campaign.objects.get(pk=c)
    try:
        camdict = Campaign.objects.filter(pk=c.id).values(*campaign_fields).first()
        camdict['categories'] = '{' + ', '.join(c.categories.names()) + '}'
        camdict['mpas'] = '{' + ', '.join([str(l) for l in c.mpas.values_list('pk', flat=True)] ) + '}'
        the_geom = c.geom
        if c.is_point:
            the_geom = c.point_geom
        lookup = {'id': c.id, 'the_geom': adaptParam(hex_or_none(the_geom)), 'geom': adaptParam(hex_or_none(c.geom)), 'point_geom': adaptParam(hex_or_none(c.point_geom)), 'columns': ', '.join(camdict.keys()), 'values': ', '.join([adaptParam(v) for v in camdict.values()])}
        upsert = '''
            UPDATE campaign SET (the_geom, geom, point_geom, %(columns)s) = (%(the_geom)s::geometry, %(geom)s::geometry, %(point_geom)s::geometry, %(values)s) WHERE id=%(id)s;
                INSERT INTO campaign (the_geom, geom, point_geom, %(columns)s)
                    SELECT %(the_geom)s::geometry, %(geom)s::geometry, %(point_geom)s::geometry, %(values)s
                    WHERE NOT EXISTS (SELECT 1 FROM campaign WHERE id=%(id)s);
        ''' % (lookup)
        return upsert
    except Exception as e:
        print('ERROR processing campaign %s: ' % c.id, e)
        raise(e)

def updateCampaign(c):
    '''Executes Campaign update/insert statements using the Carto API via the carto module.
       Returns mpa.mpa_id or None if error'''
    if not isinstance(c, Campaign):
        c = Campaign.objects.get(pk=c)
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    try:
        sql.send(updateCampaignSQL(c))
        return c.pk
    except CartoException as e:
        print('Carto Error for campaign id %s:' % c.pk, e)
    return None

def updateAllCampaigns(cams=campaigns, step=10, limit=None):
    '''Execute bulk Campaign update/insert statements using the Carto API via the carto module.
       mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
       step = number of Mpas to update per http transaction
       limit = only process a subset of records, useful for testing
       Returns list of mpa.mpa_ids that were not processed due to errors, empty list if no errors
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    numcams = cams.count()
    if limit:
        nummcams = min(limit, numcams)
    print('Processing %s of %s campaign records at a time' % (step, numcams))
    r = list(range(0,numcams+2,step))
    if r and r[-1] < numcams:
        r.append(numcams)
    error_ids = []
    start = time.time()
    for i in range(0,len(r)-1):
        r0 = r[i]
        r1 = r[i+1]
        print('Records [%s - %s]' % (r0, r1-1))
        step_ids = []
        upsert = ''
        for c in cams[r0:r1]:
            try:
                upsert += updateCampaignSQL(c)
                step_ids.append(c.pk)
            except:
                error_ids.append(c.pk)
                print('Skipping Campaign', c.pk)
        # Now update this batch of records in Carto
        try:
            sql.send(upsert)
        except CartoException as e:
            print('Carto Error for campaign ids %s:' % step_ids, e)
            print('Trying single updates.')
            for cam_id in step_ids:
                try:
                    success = updateCampaign(cam_id)
                    if not success:
                        raise CartoException
                except CartoException as e:
                    error_ids.append(cam_id)
                    print('Carto Error for campaign id %s:' % cam_id, e)
    end = time.time()
    print('TOTAL', end - start, 'sec elapsed')
    return error_ids

def purgeCartoCampaigns(cams=campaigns, dryrun=False):
    '''Execute Campaign remove statements using the Carto API via the carto module for
       mpas in the Carto mpatlas table that are not found in the passed mpas queryset.
       mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
       dryrun = [False] if true, just return list of mpa_ids to be purged but don't run SQL.
       Returns list of mpa.mpa_ids that were removed, empty list if none removed.
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    nummpas = cams.count()
    local_ids = cams.values_list('id', flat=True)
    carto_idsql = '''
        SELECT id FROM campaign ORDER BY id;
    '''
    try:
        result = sql.send(carto_idsql)
    except CartoException as e:
        print('Carto Error for getting campaign ids', e)
    carto_ids = [i['id'] for i in result['rows']]
    missing = list(set(carto_ids) - set(local_ids))
    missing.sort()
    if missing:
        deletesql = '''
            DELETE FROM campaign WHERE id IN %(missing)s;
        ''' % ({'missing': adaptParam(tuple(missing))})
        if not dryrun:
            try:
                sql.send(deletesql)
            except CartoException as e:
                print('Carto Error deleting %s campaigns:' % len(missing), e)
    return missing

def addMissingCampaigns(cams=mpas, dryrun=False):
    '''Execute Campaign remove statements using the Carto API via the carto module for
       mpas in the Carto mpatlas table that are not found in the passed mpas queryset.
       mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
       dryrun = [False] if true, just return list of mpa_ids to be purged but don't run SQL.
       Returns list of mpa.mpa_ids that were removed, empty list if none removed.
    '''
    auth_client = APIKeyAuthClient(api_key=API_KEY, base_url=USR_BASE_URL)
    sql = SQLClient(auth_client)
    numcams = cams.count()
    local_ids = cams.values_list('id', flat=True)
    carto_idsql = '''
        SELECT id FROM campaign ORDER BY id;
    '''
    try:
        result = sql.send(carto_idsql)
    except CartoException as e:
        print('Carto Error for getting campaign ids', e)
    carto_ids = [i['id'] for i in result['rows']]
    missing = list(set(local_ids) - set(carto_ids))
    missing.sort()
    if missing:
        addcams = cams.filter(id__in = missing)
        if not dryrun:
            updateAllCampaigns(addcams)
    return missing

campaign_fields = [
    'id',
    'name',
    'slug',
    #'categories',
    'country',
    'sub_location',
    'summary',
    'is_point',
    'start_year',
    'active',
    # 'mpas',
    #'point_geom',
    #'geom',
]

remote_campaign_fields = campaign_fields + ['categories'] + ['mpas']