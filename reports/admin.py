from django.contrib import admin
from .models import *


class SummonWarrentModelAdmin(admin.ModelAdmin):
    list_display = [ "order_id", "category", "police_station", "assigned_to", "due_date", "is_visited" ]
    list_filter = [ "category", "police_station", "is_visited" ]
    search_fields = ["order_id"]
admin.site.register(SummonWarrentModel, SummonWarrentModelAdmin)

admin.site.register(BeatOfficerLogs)

admin.site.register(LoactionVisitModel)
admin.site.register(PersonVisitModel)
admin.site.register(GeneralVisitModel)