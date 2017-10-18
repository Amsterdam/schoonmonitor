from django.views.generic import TemplateView
#from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from schoonmonitor.api.models import Beeldmaatlat, Melding
from schoonmonitor.api.serializers import (BeeldmaatlatSerializer,
                                         MeldingSerializer,
                                         )

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'



class BeeldmaatlatViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Employee objects """
    queryset = Beeldmaatlat.objects.all()
    serializer_class = BeeldmaatlatSerializer


class MeldingViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Employee objects """
    queryset = Melding.objects.all()
    serializer_class = MeldingSerializer
