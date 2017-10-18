from django.contrib import admin
from schoonmonitor.api.models import Beeldmaatlat
from leaflet.admin import LeafletGeoAdmin

# Change header name
admin.site.site_header = 'Schoonmonitor'

# Register your models here.



# //////////////////////////////////////////////
# Main Project
# /////////////////////////////////////////////


class BeeldmaatlattenAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_projects = ('name')
    #inlines = [WerkorderInline, ProjectPlanInline]


admin.site.register(Beeldmaatlat, BeeldmaatlattenAdmin)


