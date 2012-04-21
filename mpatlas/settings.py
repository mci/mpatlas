# Django settings for mpatlas project.

# -*- coding: utf-8 -*-
import os
#gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
SITE_PATH = os.path.dirname(PROJECT_PATH)

DEBUG = True

# Override DEBUG with local_settings.py value right away.  We override all other global
# settings with local_settings.py values at the end of this file.
try:
    from local_settings import DEBUG
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Russell Moffitt', 'Russell.Moffitt@marine-conservation.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mpatlas',                      # Or path to database file if using sqlite3.
        'USER': 'mpatlas',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Uncomment to enable caching with memcached
#CACHE_BACKEND = 'memcached://unix:/home/mpatlas/memcached.sock'
#CACHE_BACKEND = 'dummy://'
# For per-site cache (UpdateCache and FetchFromCache Middleware)
#CACHE_MIDDLEWARE_SECONDS = 4800
#CACHE_MIDDLEWARE_SECONDS = 0
CACHE_MIDDLEWARE_SECONDS = 480
CACHE_MIDDLEWARE_KEY_PREFIX = 'mpatlas'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/mpatlas/www/mpatlas/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/mpatlas/www/mpatlas/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, 'admin/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'staticfiles.finders.LegacyAppDirectoriesFinder',
)

STATICFILES_STORAGE = 'staticfiles.storage.StaticFileStorage'

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_URL = '/users/login/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    # Uncomment to enable caching with memcached
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment to enable caching with memcached
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'mpatlas.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    #'django.core.context_processors.static',
    'staticfiles.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates')
)

# TinyMCE Settings
#TINYMCE_JS_URL = os.path.join(STATIC_URL, "tiny_mce", "tiny_mce.js")
TINYMCE_FILEBROWSER = False
TINYMCE_SPELLCHECKER = False
TINYMCE_DEFAULT_CONFIG = {
    #'width' : "1000",
    #'height' : "800",
    'plugins': "table,paste,advimage,advlink",
    'extended_valid_elements' : "a[name|href|target|title|onclick|rel]",
    'theme':'advanced',
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    #'plugins' : "table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,preview,zoom,flash,searchreplace,print,contextmenu,fullscreen",
    'plugins' : "table,save,advhr,advimage,advlink,preview,searchreplace,contextmenu,fullscreen",
    #'file_browser_callback' : "CustomFileBrowser",
    #'theme_advanced_buttons1' : "code,separator,forecolor,backcolor,separator,bold,italic,underline,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,bullist,numlist,separator,undo,redo,separator,link,unlink,advimage,image,hr",
    #'theme_advanced_buttons2' : "bullist,numlist,separator,outdent,indent,separator,undo,redo,separator",
    #'theme_advanced_buttons3' : "table,row_props,cell_props,delete_col,delete_row,col_after,col_before,row_after,row_before,row_after,row_before,split_cells,merge_cells",
    'theme_advanced_buttons1' : "separator,fullscreen,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,image,cleanup,help,separator,code",
    'theme_advanced_buttons2' : "table,row_props,cell_props,delete_col,delete_row,col_after,col_before,row_after,row_before,row_after,row_before,split_cells,merge_cells",
    'theme_advanced_buttons3' : "",
    'auto_cleanup_word' : True,
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_path' : False,
    'theme_advanced_resizing' : True,
    'theme_advanced_resize_horizontal' : False,
    'theme_advanced_resizing_use_cookie' : True,
    'fullscreen_settings' : {
        'theme_advanced_path_location' : "top",
        'theme_advanced_buttons1' : "fullscreen,separator,preview,separator,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help",
        'theme_advanced_buttons2' : "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor",
        'theme_advanced_buttons3' : "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"
  }   
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    'staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
    'django_extensions',
    'storages',
    'south',
    'django.contrib.gis',
    
    'reversion',
    
    'tinymce',
    
    # User accounts and registration
    'accounts',
    
    # Spatial data
    'world',
    'wdpa',
    'usmpa',
    'mpa',
    'spatialdata',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass

