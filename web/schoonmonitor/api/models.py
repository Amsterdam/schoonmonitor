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
    crid = models.AutoField(primary_key=True)
    Schouwronde = models.CharField(max_length=255)
    Volgnummer_inspectie = models.CharField(max_length=255)
    Volgnummer_score = models.CharField(max_length=128)
    Aanmaakdatum_score = models.DateTimeField(blank=False, default=datetime.now)
    Inspecteur = models.CharField(max_length=128)
    Bestekspost = models.CharField(max_length=255)
    Score = models.CharField(max_length=4)
    brtk2015 = models.CharField(max_length=4)
    verblijfin = models.CharField(max_length=1)
    bc2015 = models.CharField(max_length=3)
    Stadsdeel = models.CharField(max_length=128)
    geb22 = models.CharField(max_length=4)
    name = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=8,
                                        decimal_places=6,
                                        blank=True,
                                        default=0.00000)
    lon = models.DecimalField(max_digits=8,
                                        decimal_places=6,
                                        blank=True,
                                        default=0.00000)
    meetgebied = models.PolygonField(srid=4326, null=True)
  #centroidegebied = models.PointField(srid=4326, null=True)

    #Account_houder = models.ForeignKey(Employee, blank=True, related_name='accountant_project', on_delete=models.CASCADE, null=True)


    # Convert manytomany list into a string 
    #@property
    #def Type(self):
    #    return ', '.join([a.Projectype for a in self.Projecttype.all()])
    
    #@property
    #def Jaar(self):
    #    return '{}'.format(self.startdatum.year)

    def __str__(self):
        return '{} - {}'.format(self.Volgnummer_inspectie, self.Bestekspost)

    objects = models.GeoManager()

    class Meta:
        get_latest_by = "Aanmaakdatum_score"
