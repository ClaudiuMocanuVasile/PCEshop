"""
Django settings for PCEshop project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$zghtd9kyde!sp^g6^!)haz8zf7f9+7v^_&z#y$uwtoi+cwdv6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['pceshop.herokuapp.com', 'localhost', '127.0.0.1', 'www.pceshop.xyz', 'pceshop.xyz']

# Email setup

EMAIL_HOST = "smtp.eu.mailgun.org"
EMAIL_HOST_USER = "postmaster@pceshop.xyz"
EMAIL_HOST_PASSWORD = "58b2a02e3c479b67c72e8bac57fbb998-fb87af35-7c5aa5fb"
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Installed apps

    'django_filters',
    'storages',
    'boto3',

    # My apps

    'shop.apps.ShopConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PCEshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'PCEshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'pceshop_database',
#         'USER': 'postgres',
#         'PASSWORD': 'superuser',
#         'HOST': 'pceshop-database.c5yqpkxycbfz.us-east-2.rds.amazonaws.com',
#         'PORT': '5432'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
# MEDIA_URL = '/images/'
# AWS_ACCESS_KEY_ID = 'AKIASJSKQZUXADQZFLVC'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'pceshop-static'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_DEFAULT_ACL = 'public-read-write'
# AWS_S3_VERIFY = True
# AWS_LOCATION = 'static'
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# DEFAULT_FILE_STORAGE = 'PCEshop.s3utils.MediaRootS3Boto3Storage'
# STATICFILES_STORAGE = 'PCEshop.s3utils.StaticRootS3Boto3Storage'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
MEDIA_URL = '/images/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
