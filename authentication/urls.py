from django.urls import path
from .views_auth import *
from .views_web import *
from .views_app import *


urlpatterns = [

	# Beat Offficer Auth
	path('app/bo-login/', bo_login, name="bo-login"),
	path('app/bo-forgot/', bo_forgot, name="bo-forgot"),
	path('app/bo-reset/', bo_reset, name="bo-reset"),
	path('app/bo-new/<joining_code>/', bo_new, name="bo-new"),
	path('app/bo-add-profile/', bo_personal_details, name="bo-add-profile"),
	path('app/bo-profile/', app_get_bo_profile, name="bo-get-profile"),

	# Officer Auth
	path('web/officer-login/', officer_login, name="officer-login"),
	path('web/officer-login-otp/', officer_login_otp, name="officer-login-otp"),
	path('web/officer-forgot/', officer_forgot, name="officer-forgot"),
	path('web/officer-reset/', officer_reset, name="officer-reset"),
	
	# Beat Area
	path('app/get-beat-areas/', app_get_beat_areas, name="get-beat-areas"),
	path('app/get-beat-area-polygons/', app_get_beat_area_polygons, name="get-beat-area-polygons"),
	path('web/get-beat-areas/', web_get_beat_areas, name="get-beat-areas"),
	path('web/get-beat-area-polygons/', web_get_beat_area_polygons, name="get-beat-area-polygons"),

	# Beat Officer Management
	path('web/get-beat-officers/', web_get_beat_officers, name="get-beat-officers"),
	path('web/add-beat-officers/', web_add_beat_officer, name="add-beat-officers"),

]