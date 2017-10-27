from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from schoonmonitor.api.models import (Beeldmaatlat, Melding
                                    )



#class BeeldmaatlatSerializer(serializers.HyperlinkedModelSerializer):
 #   """ Serializer to represent the Employee model """
 #   class Meta:
  #      model = Beeldmaatlat
   #     fields = '__all__'


class BeeldmaatlatSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = Beeldmaatlat
        geo_field = 'geom'
        fields = 'score', 'bestekspost','aanmaakdatum_score'

class MeldingSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = Melding
        geo_field = 'Geom'
        fields = 'Hoofdrubriek', 'Subrubriek', 'Datummelding'