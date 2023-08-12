from django.urls import path
from . import views
from .views import *


urlpatterns = [

	# Beat Offficer
	path('bo-login/', views.bo_login, name="bo-login"),
	path('bo-forgot/', views.bo_forgot, name="bo-forgot"),
	path('bo-reset/', views.bo_reset, name="bo-reset"),
    path('bo-profile/',views.beat_officer_profile, name="bo-profile"),

	# Officer
	path('officer-login/', views.officer_login, name="officer-login"),
	path('officer-forgot/', views.officer_forgot, name="officer-forgot"),
	path('officer-reset/', views.officer_reset, name="officer-reset"),

	path('get-beat-areas/', views.app_get_beat_areas, name="get-beat-areas"),
	# testing
	path('signup/', views.signUp, name="signup"),
    


]