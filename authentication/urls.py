from django.urls import path
from . import views
from .views import *


urlpatterns = [

	path('signup/', views.signUp, name="signup"),
	path('login/', views.logIn, name="login"),
    path('getu/', views.get_users_in_group, name="get"),
	# path('forgot/', views.forgot, name="forgot"),
	# path('reset/', views.reset, name="reset"),
	# path('verify-jwt/', views.verify_jwt, name="verify-jwt"),
    # path('verify-jwt-customer/', views.verify_jwt_customer, name="verify-jwt-customer"),
	#path('api/login/', views.api_login, name='api_login')

]