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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
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
        "ENGINE": "django.db.backends.postgresql",
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

ALLOWED_HOSTS = environ.get("ADDJ_ALLOWED_HOSTS", [])

# Localisation

LANGUAGE_CODE = environ.get("ADDJ_LANG_CODE", "en-gb")
TIME_ZONE = environ.get("ADDJ_TIMEZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True
