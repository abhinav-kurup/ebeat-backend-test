from datetime import timedelta
from decouple import config
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ["34.226.180.160"]

# Apps
INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'corsheaders',
    'channels',
    'rest_framework',
    'guardian',
    'rest_framework_simplejwt',
    # 'rest_framework_simplejwt.token_blacklist',
    'rest_framework_gis',
    'leaflet',
    'base.apps.BaseConfig',
    'authentication.apps.AuthenticationConfig',
    'app.apps.AppConfig',
    'reports.apps.ReportsConfig',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'

# Templating
TEMPLATES_DIRS = [
    os.path.join(BASE_DIR, "templates"),
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Main Settings
AUTH_USER_MODEL = 'base.BaseUser'
ASGI_APPLICATION = 'core.asgi.application'
# WSGI_APPLICATION = 'core.wsgi.application'


# Database Setup
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Language and Time 
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S' 
USE_I18N = False
USE_L10N = False
USE_TZ = False


# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join("static")
MEDIA_URL = '/data/'
MEDIA_ROOT = os.path.join("data")

# AWS Config
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_DEFAULT_ACL = None

# AWS Static Files Config
# STATIC_LOCATION = 'static'
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
# STATICFILES_STORAGE = 'core.storages.StaticStore'

# AWS Media Files Config
# PUBLIC_MEDIA_LOCATION = 'media'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
# DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'


# Geolocaiton Lib Settings
GDAL_LIBRARY_PATH = config("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = config("GEOS_LIBRARY_PATH")
SPATIALITE_LIBRARY_PATH = config("SPATIALITE_LIBRARY_PATH")


# CORS
CORS_ALLOW_ALL_ORGIN = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PATCH',
    'DELETE'
    # 'OPTIONS',
]

# CSRF_COOKIE_SAMESITE = "Lax"
# SESSION_COOKIE_SAMESITE = "Lax"
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_HTTPONLY = True

# SSL Settings
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True


# Django REST Framework
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# Auth - JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config("JWT_KEY"),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Cache
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_DB = config("REDIS_DB")
REDIS_PASSWORD = config("REDIS_PASSWORD")

CACHE_TTL = 60
DEFAULT_TIMEOUT = 60
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379/1",
        "LOCATION": f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        }
    }
}


# Email Service
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
]


# JAZZMIN_SETTINGS = {
#     # title of the window (Will default to current_admin_site.site_title if absent or None)
#     "site_title": "Library Admin",

#     # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_header": "Library",

#     # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_brand": "Library",

#     # Logo to use for your site, must be present in static files, used for brand on top left
#     "site_logo": "books/img/logo.png",

#     # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
#     "login_logo": None,

#     # Logo to use for login form in dark themes (defaults to login_logo)
#     "login_logo_dark": None,

#     # CSS classes that are applied to the logo above
#     "site_logo_classes": "img-circle",

#     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
#     "site_icon": None,

#     # Welcome text on the login screen
#     "welcome_sign": "Welcome to the library",

#     # Copyright on the footer
#     "copyright": "Acme Library Ltd",

#     # List of model admins to search from the search bar, search bar omitted if excluded
#     # If you want to use a single search field you dont need to use a list, you can use a simple string 
#     "search_model": ["auth.User", "auth.Group"],

#     # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
#     "user_avatar": None,

#     ############
#     # Top Menu #
#     ############

#     # Links to put along the top menu
#     "topmenu_links": [

#         # Url that gets reversed (Permissions can be added)
#         {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

#         # external url that opens in a new window (Permissions can be added)
#         {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

#         # model admin to link to (Permissions checked against model)
#         {"model": "auth.User"},

#         # App with dropdown menu to all its models pages (Permissions checked against models)
#         {"app": "books"},
#     ],

#     #############
#     # User Menu #
#     #############

#     # Additional links to include in the user menu on the top right ("app" url type is not allowed)
#     "usermenu_links": [
#         {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
#         {"model": "auth.user"}
#     ],

#     #############
#     # Side Menu #
#     #############

#     # Whether to display the side menu
#     "show_sidebar": True,

#     # Whether to aut expand the menu
#     "navigation_expanded": True,

#     # Hide these apps when generating side menu e.g (auth)
#     "hide_apps": [],

#     # Hide these models when generating side menu (e.g auth.user)
#     "hide_models": [],

#     # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
#     "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

#     # Custom links to append to app groups, keyed on app name
#     "custom_links": {
#         "books": [{
#             "name": "Make Messages", 
#             "url": "make_messages", 
#             "icon": "fas fa-comments",
#             "permissions": ["books.view_book"]
#         }]
#     },

#     # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
#     # for the full list of 5.13.0 free icon classes
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",
#         "auth.Group": "fas fa-users",
#     },
#     # Icons that are used when one is not manually specified
#     "default_icon_parents": "fas fa-chevron-circle-right",
#     "default_icon_children": "fas fa-circle",

#     #################
#     # Related Modal #
#     #################
#     # Use modals instead of popups
#     "related_modal_active": False,

#     #############
#     # UI Tweaks #
#     #############
#     # Relative paths to custom CSS/JS scripts (must be present in static files)
#     "custom_css": None,
#     "custom_js": None,
#     # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
#     "use_google_fonts_cdn": True,
#     # Whether to show the UI customizer on the sidebar
#     "show_ui_builder": False,

#     ###############
#     # Change view #
#     ###############
#     # Render out the change view as a single form, or in tabs, current options are
#     # - single
#     # - horizontal_tabs (default)
#     # - vertical_tabs
#     # - collapsible
#     # - carousel
#     "changeform_format": "horizontal_tabs",
#     # override change forms on a per modeladmin basis
#     "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
#     # Add a language dropdown into the admin
#     "language_chooser": False,
# }

