from django.urls import path
from .views_app import *
from .views_web import *


urlpatterns = [

# APP
	path('app/get-location-types/', app_get_location_types, name="app-get-location-types"),
	path('app/get-locations/', app_get_locations, name="app-get-locations"),
	# path('app/add-location/', app_add_location, name="app-add-location"),
	path('app/get-people/', app_get_people, name="app-get-people"),
    path('app/add-locations/',LocationAddEdit.as_view() , name="app-add-locations"),
    path('app/add-person/', PersonAddEdit.as_view(), name="app-add-person"),

# Common
	path('location/<id>/', SingleLocationView.as_view(), name="single-location"),
	path('person/<id>/', SinglePersonView.as_view(), name="single-person"),

# WEB
	path('web/get-location-types/', web_get_location_types, name="web-get-location-types"),
	path('web/get-locations/', web_get_locations, name="web-get-locations"),
	path('web/get-location-previous-incharge/<lo_id>/', web_get_previous_location_incharge, name="web-get-location-previous-incharge"),
	
	path('web/get-people/', web_get_people, name="web-get-people"),

]