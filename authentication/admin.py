from django.contrib import admin
from .models import *


class BeatOfficerModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "service_number", "phone"]
    search_fields = ["name", "email"]
admin.site.register(BeatOfficerModel, BeatOfficerModelAdmin)


class OfficerModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "service_number", "phone"]
    search_fields = ["name", "email"]
admin.site.register(OfficerModel, OfficerModelAdmin)


