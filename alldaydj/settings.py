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

SHARED_APPS = [
    "django_tenants",
    "alldaydj.tenants",
    "alldaydj.users",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "tenant_users.permissions",
    "tenant_users.tenants",
    "rest_framework",
    "django_celery_results",
]

TENANT_APPS = [
    "django.contrib.contenttypes",
    "tenant_users.permissions",
    "alldaydj",
    "rest_framework",
    "django_celery_results",
]

INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "tenants.Tenant"
TENANT_DOMAIN_MODEL = "tenants.Domain"
TENANT_USERS_DOMAIN = environ.get("ADDJ_USERS_DOMAIN")
AUTH_USER_MODEL = "users.TenantUser"
SESSION_COOKIE_DOMAIN = f".{environ.get('ADDJ_USERS_DOMAIN')}"

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
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
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": environ.get("ADDJ_DB_NAME"),
        "USER": environ.get("ADDJ_DB_USER"),
        "PASSWORD": environ.get("ADDJ_DB_PASS"),
        "HOST": environ.get("ADDJ_DB_HOST"),
        "PORT": environ.get("ADDJ_DB_PORT", 5432),
    }
}

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)


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

AUTHENTICATION_BACKENDS = ["tenant_users.permissions.backend.UserBackend"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

# The hosts we can connect to the application on.

ALLOWED_HOSTS = [f".{environ.get('ADDJ_USERS_DOMAIN')}"]

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
}

# Celery

CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = environ.get("ADDJ_TIMEZONE", "UTC")
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER = f"pyamqp://{environ.get('ADDJ_RABBIT_USER', 'guest')}:{environ.get('ADDJ_RABBIT_PASS', '')}@{environ.get('ADDJ_RABBIT_HOST', 'localhost')}:{environ.get('ADDJ_RABBIT_PORT', 5672)}/"
