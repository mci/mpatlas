from djqscsv import render_to_csv_response, write_csv
from mpa.models import Mpa

qs = Mpa.objects.filter(country='PLW')

with open('/Users/russmo/Desktop/palau_mpatlas_20141128.csv', 'w') as csv_file:
	write_csv(qs, csv_file, use_verbose_names=False)

