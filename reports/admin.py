from django.contrib import admin
from .models import *


class CourtOrderModelAdmin(admin.ModelAdmin):
    list_display = [ "order_id", "category", "police_station", "due_date" ]
    list_filter = [ "category", "police_station"]
    search_fields = ["order_id"]
admin.site.register(CourtOrderModel, CourtOrderModelAdmin)

admin.site.register(BeatOfficerLogs)



admin.site.register(PersonVisitModel)


class ProclaimationImageModelAdmin(admin.StackedInline):
    model = ProclaimaitonImagesModel
class ProclaimationModelAdmin(admin.ModelAdmin):
    list_display = ["order_id", "name", "due_date"]
    search_fields = ["order_id"]
    inlines = [ProclaimationImageModelAdmin]
admin.site.register(ProclaimationModel, ProclaimationModelAdmin)


class LoactionVisitModelAdmin(admin.ModelAdmin):
    list_display = [ "location",  "created_at","updated_at" ]
    list_filter = [ "location", "created_at"]
admin.site.register(LoactionVisitModel, LoactionVisitModelAdmin)