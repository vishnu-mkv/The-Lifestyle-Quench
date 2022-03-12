"""
Django settings for curiosity project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

DEBUG = True

if DEBUG:
    from .secrets import *
else:
    import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY if DEBUG else os.environ.get(
    'DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    "corsheaders",

    # rest framework
    'rest_framework',
    'rest_framework.authtoken',

    'users.apps.UsersConfig',
    'images.apps.ImagesConfig',
    'posts.apps.PostsConfig',

    # clean up for images
    # always at last
    'django_cleanup.apps.CleanupConfig',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Access-Control-Allow-Origin',)

ROOT_URLCONF = 'curiosity.urls'

# custom user model

AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'curiosity.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# token authentication
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.ExpiringTokenAuthentication.ExpiringTokenAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880*2

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static/'),
    ]
else:
    STATIC_ROOT = Path.joinpath(BASE_DIR, 'static/')
STATIC_URL = '/static/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# For media
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# for email services
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_USE_TLS = True
EMAIL_PORT = 587

# user activation email
DAILY_ACTIVATION_LIMIT = 10
DAILY_FORGOT_PASSWORD_EMAIL_LIMIT = 10

# Authentication token validity in hours
AUTH_TOKEN_VALIDITY = 1080

if DEBUG:
    EMAIL_HOST_USER = EMAIL_ID
    EMAIL_HOST_PASSWORD = EMAIL_APP_KEY
    AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
    FRONTEND_URL = FRONTEND_URL
else:
    EMAIL_HOST_USER = os.environ.get('EMAIL_ID')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_APP_KEY')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    FRONTEND_URL = os.environ.get('FRONTEND_URL')
    django_heroku.settings(locals())

AWS_S3_FILE_OVERRIDE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Cleaner config
CLEANER_CONFIG = {
    'ProfileImage': {
        'include': {
            'userprofile': None
        },
        'exclude': {
            'image': 'default.jpg'
        }
    },
    'PostThumbnail': {
        'include': {
            'post': None
        },
        'exclude': {
            'image': 'default.jpg'
        }
    },
    'PostImage': {
        'include': {
            'post': None
        },
        'exclude': {
            'image': 'default.jpg'
        }
    }
}

# For debug
# TOP_POST_SLUGS = ["what-is-so-awesome", "master-the-blaster", "What-is-what"]
TOP_POST_SLUGS = ["theory-of-love-in-platos-symposium",
                  "a-little-thing-called-love", "free-radical-theory-of-aging"]
