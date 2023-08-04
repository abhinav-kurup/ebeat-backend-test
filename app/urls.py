from django.urls import path
from . import views
from .views import *


urlpatterns = [

	path('get-location-types/', views.GetLocationTypes.as_view(), name="get-location-types"),
	# path('get-people-types/', views.GetPeopleTypes.as_view(), name="get-people-types"),

	path('app/get-locations/', views.app_get_locations, name="app-get-locations"),
	
    path('get-locations/', views.LocationModelListView.as_view(), name="get-locations"),
	path('location/<id>/', views.SingleLocationView.as_view(), name="single-location"),
	
    path('get-locations/', views.LocationModelListView.as_view(), name="get-locations"),
	path('location/<id>/', views.SingleLocationView.as_view(), name="single-location"),

]