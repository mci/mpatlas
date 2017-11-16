# -*- coding: utf-8 -*-

from .default_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
SITE_PATH = os.path.dirname(PROJECT_PATH)

gettext = lambda s: s

# Django settings for mpatlas project.

DEBUG = True

# CartoDB API Key, set this in local settings which is not publicly version controlled
CARTO_API_KEY ='****'

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

ADMINS = (
    ('Admin', 'admin@domain.org'),
)

# MANAGERS = ADMINS

# Email via Mandrill (MailChimp)
DEFAULT_FROM_EMAIL = 'web_robot@mpatlas.org'
SERVER_EMAIL = 'web_robot@mpatlas.org'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'admin@domain.org'
EMAIL_HOST_PASSWORD = '****'

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mpatlas',                      # Or path to database file if using sqlite3.
        'USER': 'mpatlas',                      # Not used with sqlite3.
        'PASSWORD': '****',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Uncomment to enable caching with memcached
CACHE_BACKEND = 'memcached://mpatlas-memcache.aaaa.0001.usw1.cache.amazonaws.com:11211'
#CACHE_BACKEND = 'dummy://'
CACHE_MIDDLEWARE_SECONDS = 2 * 60 / 1000
CACHE_MIDDLEWARE_KEY_PREFIX = 'mpatlas_dev2'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

STORAGES_S3BOTO_MULTI = {
    'media' : {
        'AWS_ACCESS_KEY_ID' : '****',
        'AWS_SECRET_ACCESS_KEY' : '****',
        'AWS_STORAGE_BUCKET_NAME' : 'mpatlas',
        'AWS_LOCATION' : 'media',
    },
    'static' : {
        'AWS_ACCESS_KEY_ID' : '****',
        'AWS_SECRET_ACCESS_KEY' : '****',
        'AWS_STORAGE_BUCKET_NAME' : 'mpatlas',
        'AWS_LOCATION' : 'static',
    }
}

MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir, 'media/'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir, 'static/'))
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, 'admin/')

CKEDITOR_UPLOAD_PATH = 'media-uploads/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*****'

