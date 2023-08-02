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
    'rest_framework_simplejwt',
    'rest_framework_gis',
    'leaflet',
    'base.apps.BaseConfig',
    'authentication.apps.AuthenticationConfig',
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
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'your_db_name',
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }


# Auth
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
GDAL_LIBRARY_PATH = "/opt/homebrew/Cellar/gdal/3.7.1/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/opt/homebrew/Cellar/geos/3.12.0/lib/libgeos.dylib"
SPATIALITE_LIBRARY_PATH = "/usr/local/lib/mod_spatialite.dylib"


# CORS
CORS_ALLOW_ALL_ORGIN = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "https://admin-dashboard-goa-police.netlify.app/"
# ]

CORS_ALLOW_METHODS = [
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'DELETE'
]


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
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

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
CACHE_TTL = 60
DEFAULT_TIMEOUT = 60
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Service
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'us2.smtp.mailhostbox.com'
EMAIL_HOST = config("EMAIL_HOST")
# EMAIL_PORT = 25
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

