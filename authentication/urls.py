from django.urls import path
from . import views
from .views import *


urlpatterns = [

	# Beat Offficer
	path('bo-login/', views.bo_login, name="bo-login"),
	path('bo-forgot/', views.bo_forgot, name="bo-forgot"),
	path('bo-reset/', views.bo_reset, name="bo-reset"),

	# Officer
	path('officer-login/', views.officer_login, name="officer-login"),
	path('officer-forgot/', views.officer_forgot, name="officer-forgot"),
	path('officer-reset/', views.officer_reset, name="officer-reset"),

	# testing
	# path('signup/', views.signUp, name="signup"),
]