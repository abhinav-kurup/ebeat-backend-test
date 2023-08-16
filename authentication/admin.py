from leaflet.admin import LeafletGeoAdminMixin
from django.contrib import admin
from .models import *


class BeatOfficerModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "service_number", "phone", "tid"]
    search_fields = ["name", "email"]
admin.site.register(BeatOfficerModel, BeatOfficerModelAdmin)


class OfficerModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "service_number", "phone"]
    search_fields = ["name", "email"]
admin.site.register(OfficerModel, OfficerModelAdmin)


class BeatAreaModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "beat_no"]
admin.site.register(BeatAreaModel, BeatAreaModelAdmin)

class PoliceStationModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "pi"]
admin.site.register(PoliceStationModel, PoliceStationModelAdmin)

class SubDivisionModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "dysp"]
admin.site.register(SubDivisionModel, SubDivisionModelAdmin)

class DistrictModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "sp"]
admin.site.register(DistrictModel, DistrictModelAdmin)

class StateModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "igp"]
admin.site.register(StateModel, StateModelAdmin)
