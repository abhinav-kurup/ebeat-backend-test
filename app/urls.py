from django.urls import path
from .views_app import *
from .views_web import *


urlpatterns = [

# APP
	path('app/get-location-types/', app_get_location_types, name="app-get-location-types"),
	path('app/get-locations/', app_get_locations, name="app-get-locations"),
	# path('app/add-location/', app_add_location, name="app-add-location"),

	path('app/get-person-types/', app_get_person_types, name="app-get-person-types"),
	path('app/get-people/', app_get_people, name="app-get-people"),

	path('location/<id>/', SingleLocationView.as_view(), name="single-location"),
	path('person/<id>/', SinglePersonView.as_view(), name="single-person"),
    path('app/add-person/', app_add_person, name="app-add-person"),

# WEB
	path('web/get-location-types/', web_get_location_types, name="web-get-location-types"),
	# path('web/get-locations/', web_get_locations, name="web-get-locations"),
	
	
	path('web/test/', test, name="web-test"),

]