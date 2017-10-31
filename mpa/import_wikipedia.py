from __future__ import print_function
import csv, os
from .models import Mpa, Contact, WikiArticle

def import_wikipedia():
    wikifilename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Wikipedia_Matches_20120214_v2.csv'))
    wikifile = open(wikifilename, "rU")
    wikireader = csv.reader(wikifile, csv.excel)
    line = -1
    for row in wikireader:
        line += 1
        if line == 0:
            continue
        wdpa_id = row[0]
        title = row[1]
        url = row[2]
        summary = row[10]
        try:
            mpa = Mpa.objects.get(wdpa_id=wdpa_id)
        except:
            try:
                mpa = Mpa.objects.get(usmpa_id=wdpa_id)
            except:
                continue
        wiki = WikiArticle.objects.get_or_create(mpa=mpa)[0]
        wiki.url = url
        wiki.title = title
        wiki.summary = summary
        print(line, title, url)
        wiki.save()
