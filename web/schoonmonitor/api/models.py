#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime

# /////////////////////////////////////////////////
# Option menu's
# /////////////////////////////////////////////////

class Melding(models.Model):
    mid = models.AutoField(primary_key=True)
    meldingnummer = models.CharField(max_length=15, blank=True)
    Buurtcode = models.CharField(max_length=4, blank=True)
    Stadsdeelcode = models.CharField(max_length=1, blank=True)
    Afhandeltermijn = models.DecimalField(max_digits=3,
                                        decimal_places=0,
                                        blank=True,
                                        default=0)
    Buurtnaam = models.CharField(max_length=255) 
    Datummelding =  models.DateField(blank=False, default=datetime.now)
    Hoofdrubriek = models.CharField(max_length=255)
    lat = models.CharField(max_length=255) 
    lon = models.CharField(max_length=255) 
    Straat = models.CharField(max_length=255)
    Subrubriek = models.CharField(max_length=255)
    Trefwoord = models.CharField(max_length=255)
    Geom = models.PointField(srid=4326, null=True)

# /////////////////////////////////////////////////
# Main Project
# /////////////////////////////////////////////////

class Beeldmaatlat(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    aanmaakdatum_score = models.TextField(db_column='Aanmaakdatum score', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    adres = models.TextField(db_column='Adres', blank=True, null=True)  # Field name made lowercase.
    bestekspost = models.TextField(db_column='Bestekspost', blank=True, null=True)  # Field name made lowercase.
    containertype = models.TextField(db_column='Containertype', blank=True, null=True)  # Field name made lowercase.
    eigenaar = models.TextField(db_column='Eigenaar', blank=True, null=True)  # Field name made lowercase.
    fractie = models.TextField(db_column='Fractie', blank=True, null=True)  # Field name made lowercase.
    id = models.FloatField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    id_nummer = models.TextField(db_column='ID-nummer', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    inspecteur = models.TextField(db_column='Inspecteur', blank=True, null=True)  # Field name made lowercase.
    meetlocatienummer = models.FloatField(db_column='Meetlocatienummer', blank=True, null=True)  # Field name made lowercase.
    meetpunt = models.FloatField(db_column='Meetpunt', blank=True, null=True)  # Field name made lowercase.
    plusteams = models.TextField(db_column='Plusteams', blank=True, null=True)  # Field name made lowercase.
    schouwronde = models.TextField(db_column='Schouwronde', blank=True, null=True)  # Field name made lowercase.
    score = models.TextField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    serienummer = models.TextField(db_column='Serienummer', blank=True, null=True)  # Field name made lowercase.
    straat = models.TextField(db_column='Straat', blank=True, null=True)  # Field name made lowercase.
    uitmarkt = models.TextField(db_column='Uitmarkt', blank=True, null=True)  # Field name made lowercase.
    volgnummer_inspectie = models.BigIntegerField(db_column='Volgnummer inspectie', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    volgnummer_score = models.FloatField(db_column='Volgnummer score', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    volume_containertype = models.FloatField(db_column='Volume containertype', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    well_id = models.FloatField(db_column='Well ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    well_id_c = models.TextField(db_column='Well ID c', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    well_id_customer = models.TextField(db_column='Well ID customer', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    address = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    id_0 = models.IntegerField(db_column='id', primary_key=True)  # Field renamed because of name conflict.
    geom = models.GeometryField(srid=28992, blank=True, null=True)
    stadsdeelcode = models.CharField(max_length=255, blank=True, null=True)
    buurtcode = models.TextField(blank=True, null=True)
    wijkcode = models.CharField(max_length=255, blank=True, null=True)
    stadsdeelnaam = models.CharField(max_length=255, blank=True, null=True)
    buurtnaam = models.CharField(max_length=255, blank=True, null=True)
    wijknaam = models.CharField(max_length=255, blank=True, null=True)
    gebiedsnaam = models.CharField(max_length=255, blank=True, null=True)
    gebiedscode = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crowscores_totaal'
        get_latest_by = "Aanmaakdatum_score"
    def __str__(self):
        return '{} - {}'.format(self.volgnummer_inspectie, self.bestekspost)

    objects = models.GeoManager()
        
