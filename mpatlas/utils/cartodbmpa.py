import sys, json, time
from cartodb import CartoDBAPIKey, CartoDBException
from mpa.models import Mpa
from psycopg2.extensions import adapt
from django.contrib.gis import geos

API_KEY ='485144583b0c0fda73509f91ec81762f8d6a188a'
cartodb_domain = 'mpatlas'

# fields variable is overwritten at end of module, listing all fields needed to pull from mpatlas
# via a .values(*fields) call.  Update this for new columns.
fields = []

# default queryset to use for syncing from mpatlas to CartoDB
mpas = Mpa.objects.exclude(verification_state='Rejected as MPA').exclude(geom__isnull=True).order_by('-mpa_id').only('mpa_id')

def adaptParam(p):
	'''Convert and escape python objects for use in Postgresql SQL statements.
       Uses the psycopg2.extensions.adapt function rather than using param
       substitution at the database cursor level or other Django internals.
       This should provide reasonable SQL injection protection with the
       flexibility to generate and send CartoDB SQL statements via http.
	'''
	a = p
	if isinstance(p, geos.GEOSGeometry):
		p = p.wkt
	try:
		p = unicode.encode(p, 'utf-8')
	except:
		pass
	try:
		a = adapt(p).getquoted()
	except UnicodeEncodeError:
		try:
			a = adapt(unicode.encode(json.loads(json.dumps(p)), 'utf-8'))
		except:
			pass
	return a

def updateMpaSQL(m):
	'''Returns a Postgresql SQL statement that will update or insert an Mpa record
	   from the MPAtlas database into the mpatlas table on CartoDB.  The CartoDB
	   mpatlas table columns are not a one-to-one match with mpa_mpa columns.
	'''
	if not isinstance(m, Mpa):
		m = Mpa.objects.get(pk=m)
	try:
		mpadict = Mpa.objects.filter(pk=m.mpa_id).values(*fields).first()
		mpadict['categories'] = '{' + ', '.join(m.categories.names()) + '}'
		lookup = {'mpa_id': m.mpa_id, 'geom': m.geom.hexewkb, 'columns': ', '.join(mpadict.keys()), 'values': ', '.join([adaptParam(v) for v in mpadict.values()])}
		upsert = '''
			UPDATE mpatlas SET (the_geom, %(columns)s) = (ST_GeomfromEWKB(decode('%(geom)s', 'hex')), %(values)s) WHERE mpa_id=%(mpa_id)s;
				INSERT INTO mpatlas (the_geom, %(columns)s)
					SELECT ST_GeomfromEWKB(decode('%(geom)s', 'hex')), %(values)s
					WHERE NOT EXISTS (SELECT 1 FROM mpatlas WHERE mpa_id=%(mpa_id)s);
		''' % (lookup)
		return upsert
	except Exception as e:
		print 'ERROR processing mpa %s: ' % m.mpa_id, e
		raise(e)

def updateMpa(m):
	'''Executes Mpa update/insert statements using the CartoDB API via the cartodb module.
	   Returns mpa.mpa_id or None if error'''
	if not isinstance(m, Mpa):
		m = Mpa.objects.get(pk=m)
	cl = CartoDBAPIKey(API_KEY, cartodb_domain)
	try:
		cl.sql(updateMpaSQL(m))
		return m.pk
	except CartoDBException as e:
		print 'CartoDB Error for mpa_id %s:' % m.pk, e
	return None

def updateAllMpas(mpas=mpas, step=10, limit=None):
	'''Execute bulk Mpa update/insert statements using the CartoDB API via the cartodb module.
	   mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
	   step = number of Mpas to update per http transaction
	   limit = only process a subset of records, useful for testing
	   Returns list of mpa.mpa_ids that were not processed due to errors, empty list if no errors
	'''
	cl = CartoDBAPIKey(API_KEY, cartodb_domain)
	nummpas = mpas.count()
	if limit:
		nummpas = min(limit, nummpas)
	print 'Processing %s of %s mpa records at a time' % (step, nummpas)
	r = range(0,nummpas+2,step)
	if r and r[-1] < nummpas:
		r.append(nummpas)
	error_ids = []
	start = time.time()
	for i in xrange(0,len(r)-1):
		r0 = r[i]
		r1 = r[i+1]
		print 'Records [%s - %s]' % (r0, r1-1)
		step_ids = []
		upsert = ''
		for m in mpas[r0:r1]:
			try:
				upsert += updateMpaSQL(m)
				step_ids.append(m.pk)
			except:
				error_ids.append(m.pk)
				print 'Skipping Mpa', m.pk
		# Now update this batch of records in CartoDB
		try:
			cl.sql(upsert)
		except CartoDBException as e:
			print 'CartoDB Error for mpa_ids %s:' % step_ids, e
			print 'Trying single updates.'
			for mpa_id in step_ids:
				try:
					updateMpa(mpa_id)
				except CartoDBException as e:
					error_ids.append(mpa_id)
					print 'CartoDB Error for mpa_id %s:' % mpa_id, e
	end = time.time()
	print 'TOTAL', end - start, 'sec elapsed'
	return error_ids

def purgeCartoDBMpas(mpas=mpas, dryrun=False):
	'''Execute Mpa remove statements using the CartoDB API via the cartodb module for
	   mpas in the CartoDB mpatlas table that are not found in the passed mpas queryset.
	   mpas = Mpa queryset [default is all non-rejected MPAs with geom boundaries]
	   dryrun = [False] if true, just return list of mpa_ids to be purged but don't run SQL.
	   Returns list of mpa.mpa_ids that were removed, empty list if none removed.
	'''
	cl = CartoDBAPIKey(API_KEY, cartodb_domain)
	nummpas = mpas.count()
	local_ids = mpas.values_list('mpa_id', flat=True)
	cartodb_idsql = '''
		SELECT mpa_id FROM mpatlas ORDER BY mpa_id;
	'''
	try:
		result = cl.sql(cartodb_idsql)
	except CartoDBException as e:
		error_ids.extend(step_ids)
		print('CartoDB Error for getting mpa_ids', e)
	cartodb_ids = [i['mpa_id'] for i in result['rows']]
	missing = list(set(cartodb_ids) - set(local_ids))
	missing.sort()
	deletesql = '''
		DELETE FROM mpatlas WHERE mpa_id IN %(missing)s;
	''' % ({'missing': adaptParam(tuple(missing))})
	if not dryrun:
		try:
			cl.sql(deletesql)
		except CartoDBException as e:
			error_ids.extend(step_ids)
			print 'CartoDB Error deleting %s mpas:' % len(missing), e
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