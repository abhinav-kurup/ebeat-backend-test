from django.urls import path
from .views_auth import *
from .views_main import *


urlpatterns = [

	# Beat Offficer
	path('bo-login/', bo_login, name="bo-login"),
	path('bo-forgot/', bo_forgot, name="bo-forgot"),
	path('bo-reset/', bo_reset, name="bo-reset"),

	# Officer
	path('web/officer-login/', officer_login, name="officer-login"),
	path('web/officer-login-otp/', officer_login_otp, name="officer-login-otp"),
	path('web/officer-forgot/', officer_forgot, name="officer-forgot"),
	path('web/officer-reset/', officer_reset, name="officer-reset"),

	path('app/get-beat-areas/', app_get_beat_areas, name="get-beat-areas"),
	path('app/get-beat-area-polygons/', app_get_beat_area_polygons, name="get-beat-area-polygons"),

	# path('web/add-beat-officer/', web_add_beat_officer, name="add-beat-officer"),
	# testing
	# path('signup/', signUp, name="signup"),
]