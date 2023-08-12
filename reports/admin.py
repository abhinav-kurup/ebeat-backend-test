from django.contrib import admin
from .models import *


class SummonWarrentModelAdmin(admin.ModelAdmin):
    list_display = [ "order_id", "category", "police_station", "assigned_to", "due_date", "is_visited" ]
    list_filter = [ "category", "police_station", "is_visited" ]
    search_fields = ["order_id"]
admin.site.register(SummonWarrentModel, SummonWarrentModelAdmin)

admin.site.register(BeatOfficerLogs)

class LoactionVisitModelAdmin(admin.ModelAdmin):
    list_display = [ "location", "situation", "created_at"]
    list_filter = [ "location", "created_at" ]
admin.site.register(LoactionVisitModel, LoactionVisitModelAdmin)

class PersonVisitModelAdmin(admin.ModelAdmin):
    list_display = [ "person", "situation", "created_at"]
    list_filter = [ "person", "created_at" ]
admin.site.register(PersonVisitModel, PersonVisitModelAdmin)

admin.site.register(GeneralVisitModel)