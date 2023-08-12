from django.contrib import admin
from .models import *


class SummonWarrentModelAdmin(admin.ModelAdmin):
    list_display = [ "order_id", "category", "police_station", "due_date" ]
    list_filter = [ "category", "police_station"]
    search_fields = ["order_id"]
admin.site.register(SummonWarrentModel, SummonWarrentModelAdmin)

admin.site.register(BeatOfficerLogs)

admin.site.register(LoactionVisitModel)

admin.site.register(PersonVisitModel)
