"""
Django Settings for AllDay DJ.
"""

from distutils.util import strtobool
from os import environ
from pathlib import Path

# Unique secret key per instalation

SECRET_KEY = environ.get("ADDJ_SECRET_KEY")

# Debug more

DEBUG = strtobool(environ.get("ADDJ_DEBUG", "False"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_celery_results",
    "colorfield",
    "django_nose",
    "corsheaders",
    "alldaydj",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "alldaydj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "alldaydj.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": environ.get("ADDJ_DB_NAME"),
        "USER": environ.get("ADDJ_DB_USER"),
        "PASSWORD": environ.get("ADDJ_DB_PASS"),
        "HOST": environ.get("ADDJ_DB_HOST"),
        "PORT": environ.get("ADDJ_DB_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

# The hosts we can connect to the application on.

ALLOWED_HOSTS = [environ.get("ADDJ_USERS_DOMAIN"), "localhost"]

# Localisation

LANGUAGE_CODE = environ.get("ADDJ_LANG_CODE", "en-gb")
TIME_ZONE = environ.get("ADDJ_TIMEZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# REST Framework

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissions",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

# Celery

CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = environ.get("ADDJ_TIMEZONE", "UTC")
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER = f"pyamqp://{environ.get('ADDJ_RABBIT_USER', 'guest')}:{environ.get('ADDJ_RABBIT_PASS', '')}@{environ.get('ADDJ_RABBIT_HOST', 'localhost')}:{environ.get('ADDJ_RABBIT_PORT', 5672)}/"
CELERY_ALWAYS_EAGER = strtobool(environ.get("ADDJ_CELERY_ALWAYS_EAGER", "False"))

# Nose

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=alldaydj",
    "--cover-xml",
    "--verbosity=2",
]

# File Storage

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_REGION_NAME = environ.get("ADDJ_S3_REGION")
AWS_S3_ENDPOINT_URL = environ.get("ADDJ_S3_ENDPOINT")
AWS_ACCESS_KEY_ID = environ.get("ADDJ_S3_KEY_ID")
AWS_SECRET_ACCESS_KEY = environ.get("ADDJ_S3_KEY_SECRET")
AWS_STORAGE_BUCKET_NAME = environ.get("ADDJ_S3_BUCKET")
AWS_QUERYSTRING_AUTH = False

# AllDay DJ

ADDJ_DEFAULT_PERMISSIONS = [
    "add_artist",
    "change_artist",
    "delete_artist",
    "view_artist",
    "add_cart",
    "change_cart",
    "delete_cart",
    "view_cart",
    "add_tag",
    "change_tag",
    "delete_tag",
    "view_tag",
    "add_type",
    "change_type",
    "delete_type",
    "view_type",
]

ADDJ_DEFAULT_GROUP = environ.get("ADDJ_DEFAULT_GROUP", "alldaydj_users")
ADDJ_COMPRESSED_MIME_TYPES = ["FLAC", "ID3", "AAC", "Ogg data, Vorbis audio"]
ADDJ_OGG_QUALITY = int(environ.get("ADDJ_OGG_QUALITY", "4"))

# CORS

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https?://localhost:\d+$",
    f"^https?://{environ.get('ADDJ_USERS_DOMAIN')}$",
]
