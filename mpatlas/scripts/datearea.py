from mpa.models import Mpa
import csv

outfields = (
    'mpa_id', 'name', 'designation', 'designation_eng', 'designation_type', 
    'iucn_category', 'country', 'sub_location', 'verification_state', 'verification_reason', 'status', 'status_year', 
    'no_take_area', 'rep_m_area', 'calc_m_area', 'rep_area', 'calc_area'
)

def run():
    encoding = 'utf8'
    outfile = open('/home/mpatlas/datearea.csv', 'wb')
    csvWriter = csv.writer(outfile, dialect=csv.excel)
    header = [unicode(u'%s' % f).encode(encoding) for f in outfields]
    csvWriter.writerow(header)
    for mpa in Mpa.objects.all().order_by('status_year', 'name').only(*outfields):
        output = [unicode(getattr(mpa, f)).encode(encoding) if (getattr(mpa, f) is not None) else '' for f in outfields]
        csvWriter.writerow(output)
    outfile.close()
    return open('/tmp/datearea.csv', 'r')
