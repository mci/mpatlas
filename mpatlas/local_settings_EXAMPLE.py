DEBUG = False

ADMINS = (
    # ('Your Name', 'you@yourcompany.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mpatlas',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STORAGES_S3BOTO_MULTI = {
    'media' : {
        'AWS_ACCESS_KEY_ID' : 'key',
        'AWS_SECRET_ACCESS_KEY' : 'secret',
        'AWS_STORAGE_BUCKET_NAME' : 'mybucket',
        'AWS_LOCATION' : 'media',
    },
    'static' : {
        'AWS_ACCESS_KEY_ID' : 'key',
        'AWS_SECRET_ACCESS_KEY' : 'secret',
        'AWS_STORAGE_BUCKET_NAME' : 'mybucket',
        'AWS_LOCATION' : 'static',
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_media'
STATICFILES_STORAGE = 'storages.backends.s3botomulti.S3BotoStorage_static'

# MEDIA and STATIC settings for S3/CloudFront
MEDIA_ROOT = '/home/myuser/www/myproject/media/'
MEDIA_URL = '//cdn.myproject.org/media/'
STATIC_ROOT = '/home/myuser/www/myproject/static/'
STATIC_URL = '//cdn.myproject.org/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret'
