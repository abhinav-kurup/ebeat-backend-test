from django.urls import path
from .views_app import *
from .views_web import *


urlpatterns = [

	# Location Visits
	path('app/add-location-visit/', app_add_location_visit, name="app-add-location-visit"),
	path('app/get-location-visits/', app_get_location_visits, name="app-get-location-visits"),
	path('app/location-visit/<pk>/', get_location_visit_detail, name="app-get-location-visit-details"),
    
	# Person Visits
	path('app/add-person-visit/', app_add_person_visit, name="app-add-person-visit"),
	path('app/get-person-visits/', app_get_person_visits, name="app-get-person-visits"),
	path('app/person-visit/<pk>/', get_person_report_single, name="app-get-person-visit-details"),
    
	# Court Orders
	path('app/court-order/<pk>/', app_court_order_detail, name="app-get-court-order-details"),
    
	# Logs
	path('app/calendar-view/<mo>/<yr>/', get_log_dates, name="app-calendar-view"),
	path('app/add-log/', app_add_logs, name="app-add-log"),
	path('app/get-logs/<dt>/', app_get_logs, name="app-get-logs"),

]