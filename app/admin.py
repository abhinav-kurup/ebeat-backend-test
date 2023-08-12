from leaflet.admin import LeafletGeoAdminMixin
from django.contrib import admin
from .models import *


admin.site.register(LocationCategoryModel)
admin.site.register(PersonTypeModel)


class LocationInchargeModelAdmin(admin.StackedInline):
    model = LocationInchargeModel
class LocationModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "type", "is_active"]
    list_filter = ["type", "is_active"]
    search_fields = ["name", "address"]
    inlines = [LocationInchargeModelAdmin]
admin.site.register(LocationModel, LocationModelAdmin)


class PersonModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "address"]
admin.site.register(PersonModel, PersonModelAdmin)
