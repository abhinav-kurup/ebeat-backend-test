from django.urls import path
from . import views
from .views import *


urlpatterns = [
	
	path('app/add-locations/', views.add_locations, name="app-add-locations"),
	
    path('app/get-location-types/', views.app_get_location_types, name="app-get-location-types"),
    path('app/add-location/', views.add_locations, name="app-add-location"),

	path('app/get-locations/', views.app_get_locations, name="app-get-locations"),
	
    # path('get-locations/', views.LocationModelListView.as_view(), name="get-locations"),
	path('location/<id>/', views.SingleLocationView.as_view(), name="single-location"),
    
	#persons
	path('app/get-persons/', views.app_get_person, name="app-get-person"),
    path('app/get-person-types/', views.app_get_person_types, name="app-get-person-types"),
    path('person/<id>/', views.SinglePersonView.as_view(), name="single-person"),
    
    
	#reports
	path('app/add-location-report/', views.add_location_reports, name="app-add-location-report"),
    path('app/get-location-reports/', views.get_location_reports, name="app-get-location-reports"),
    path('app/get-location-detail-reports/', views.get_location_detail_reports, name="app-get-location-detail-reports"),

    path('app/add-person-report/', views.add_person_reports, name="app-add-person-report"),
    path('app/get-person-reports/', views.get_person_reports, name="app-get-person-reports"),
    path('app/get-person-detail-reports/', views.get_person_detail_reports, name="app-get-person-detail-reports"),
    
	#summons
    path('app/get-summons/', views.app_get_summons, name="app-get-summons"),
    path('app/get-summon-details/', views.app_summons_details, name="app-get-summon-details"),

    #logs
    path('app/get-logs/', views.app_get_logs, name="app-get-logs"),
    path('app/add-logs/', views.app_add_logs, name="app-add-logs"),
    path('app/log-dates/', views.get_log_dates, name="app-get-log-dates"),
	
	#WEB
	path('web/get-locations/', views.web_get_locations, name="web-get-locations"),
    path('web/get-location-types/', views.web_get_location_types, name="web-get-location-types"),
    path('web/get-location-names/', views.web_get_location_names, name="web-get-location-names"),
    path('web/get-location-details/', views.web_location_detail, name="web-get-location-details"),
    path('web/get-location-reports/', views.web_location_reports, name="web-get-location-reports"),
    path('web/get-location-report-details/', views.web_location_report_detail, name="web-get-location-report-details"),
]