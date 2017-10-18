import csv, sys, os

project_dir = 'data'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'schoonmonitor.settings'

import django

django.setup()

from schoonmonitor.api.models import Beeldmaatlat, Melding

data = csv.reader(open('data/crowscores.csv'), delimiter = ';')
next(data) # skip header
for row in data:
    print(row)
    post = Beeldmaatlat()
    post.crid = row[0]
    post.Schouwronde = row[1], 
    post.Volgnummer_inspectie = row[2]
    post.Volgnummer_score = row[3]
    post.Aanmaakdatum_score = row[4]
    post.Inspecteur = row[5]
    post.Bestekspost = row[6]
    post.Score = row[7]
    post.brtk2015=row[8]
    post.verblijfin=row[9]
    post.bc2015=row[10]
    post.Stadsdeel=row[11]
    post.geb22 = row[12]
    post.name = row[13]
    post.lat = row[14]
    post.lon =row[15]
    post.meetgebied=row[16]
    post.save()


moraData = csv.reader(open('data/MORA.csv'), delimiter = ';')
next(moraData) # skip header
for row in moraData:  
    print(row)
    post = Melding()  
    post.mid = row[0]
    post.meldingnummer = row[1]
    post.Buurtcode = row[2]
    post.Stadsdeelcode = row[3]
    post.Afhandeltermijn = row[4]
    post.Buurtnaam = row[5] 
    post.Datummelding = row[6]
    post.Hoofdrubriek = row[7]
    post.lat = row[8] 
    post.lon = row[9] 
    post.Straat = row[10]
    post.Subrubriek = row[11]
    post.Trefwoord = row[12]
    post.Geom = row[13]
    post.save()