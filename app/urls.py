from django.urls import path
from . import views
from .views import *


urlpatterns = [

	path('get-location-types/', views.GetLocationTypes.as_view(), name="get-location-types"),
	
    path('get-locations/', views.LocationModelListView.as_view(), name="get-locations"),
	path('location/<id>/', views.SingleLocationView.as_view(), name="single-location"),

]