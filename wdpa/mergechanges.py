from wdpa import merge
from mpa.models import Mpa, mpas_all_nogeom, VersionMetadata, mpa_post_save
from mpa import admin as mpa_admin # needed to kick in reversion registration

import reversion
from reversion.models import Revision

import datetime
import json

removelist = merge.getRemoveWdpaList()
addlist = merge.getAddWdpaList()
updatelist = merge.getUpdateWdpaList()

existingrevisions = {}

merge.removeMpasByWdpaId(removelist)
merge.updateMpasFromWdpaList(ids=addlist, existingrevisions=existingrevisions)
merge.updateMpasFromWdpaList(ids=updatelist, existingrevisions=existingrevisions)

# load changelist
removelist = []
addlist = []
updatelist = []
existingrevisions = {}
with open('/home/mpatlas/wdpa2014_removed.json', 'r') as removefile:
	removelist = json.load(removefile)
with open('/home/mpatlas/wdpa2014_added.json', 'r') as addfile:
	addlist = json.load(addfile)
with open('/home/mpatlas/wdpa2014_updated.json', 'r') as updatefile:
	updatelist = json.load(updatefile)
with open('/home/mpatlas/wdpa2014_dataconflicts.json', 'r') as existingfile:
	existingrevisions = json.load(existingfile)

# mpa_id codes
# 99##### = wdpa removed and no revisions >> just delete it for good
# 88##### = wdpa removed but has revision >> reject with reason 'removed from wdpa but mpatlas has revision - please review'
# 77##### = wdpa updated but mpatlas has revision, this is the mpatlas revision that needs to be compared

# 600##### = mpatlas updated this record after database freeze, compare one by one to restore
# 688##### = mpatlas updated recently, but it probably should be removed
# 677##### = wdpa updated but mpatlas has recent revision

## figure out recently updated sites
datelimit = datetime.datetime(2014,11,17)
mpas = mpas_all_nogeom
for m in mpas:
	try:
		versions = reversion.get_for_object(m)
	    numversions = len(versions)
	except:
	    numversions = 0
	if numversions > 0:
		revdate = versions[0].revision.date_created
		if revdate >= datelimit:
			print m.pk
			m = Mpa.objects.get(pk=m.pk)
			m.pk = 60000000 + m.pk
			m.save()

# tag removes
removes = mpas_all_nogeom.filter(wdpa_id__in = removelist)
for m in removes:
	try:
		versions = reversion.get_for_object(m)
	    numversions = len(versions)
	except:
	    numversions = 0
	if numversions > 0 or m.pk >= 60000000:
		print m.pk
		m = Mpa.objects.get(pk=m.pk)
		m.pk = 8800000 + m.pk
		m.save()
# don't code straight deletes without revisions, we're not updating them

# tag adds with previous mpatlas revisions the same as other updates
adds = mpas_all_nogeom.filter(wdpa_id__in = addlist)
for m in adds:
	if str(m.wdpa_id) in existingrevisions or m.pk >= 60000000:
		print m.pk
		m = Mpa.objects.get(pk=m.pk)
		m.pk = 7700000 + m.pk
		m.save()
# done with add tagging

# tag updates with previous mpatlas revisions
updates = mpas_all_nogeom.filter(wdpa_id__in = updatelist)
for m in updates:
	if str(m.wdpa_id) in existingrevisions or m.pk >= 60000000:
		print m.pk
		m = Mpa.objects.get(pk=m.pk)
		m.pk = 7700000 + m.pk
		m.save()
# done with update tagging

# eliminate duplicates
dups = []
mpas = mpas_all_nogeom.filter(pk__gte=68800000)
for m in mpas:
	altpk = m.pk - 60000000
	try:
		n = Mpa.objects.get(pk=altpk)
		dups.append(n.pk)
	except:
		pass
	altpk = m.pk - 8800000
	try:
		n = Mpa.objects.get(pk=altpk)
		dups.append(n.pk)
	except:
		pass
mpas = mpas_all_nogeom.filter(pk__gte=67700000, pk__lt=68800000)
for m in mpas:
	altpk = m.pk - 60000000
	try:
		n = Mpa.objects.get(pk=altpk)
		dups.append(n.pk)
	except:
		pass
	altpk = m.pk - 7700000
	try:
		n = Mpa.objects.get(pk=altpk)
		dups.append(n.pk)
	except:
		pass
dupmpas = mpas_all_nogeom.filter(pk__in=dups)
dupmpas.delete()

# delete any old mpas that remain unchanged, we just want our change list remaining with tweaked mpa_id values
oldmpas = mpas_all_nogeom.filter(pk__lt=1100000)
oldmpas.delete()

# to export just this data, use management command to dumpdata, then use loaddata in the new database
# ./manage.py dumpdata mpa > /home/mpatlas/changedmpas.json
# ./manage.py loaddata --ignorenonexistent changedmpas.json
