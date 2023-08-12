from leaflet.admin import LeafletGeoAdminMixin
from django.contrib import admin
from .models import *


admin.site.register(LocationCategoryModel)

class LocationInchargeModelAdmin(admin.StackedInline):
    model = LocationInchargeModel
admin.site.register(LocationInchargeModel)

class LocationModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "type", "type", "is_active"]
    list_filter = ["type", "is_active"]
    search_fields = ["name"]
    inlines = [LocationInchargeModelAdmin]
admin.site.register(LocationModel, LocationModelAdmin)



admin.site.register(PersonTypeModel)
class PersonModelAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ["name", "type", "is_active"]
    list_filter = ["type", "is_active"]
    search_fields = ["name"]
    #inlines = [LocationInchargeModelAdmin]
admin.site.register(PersonModel, PersonModelAdmin)
