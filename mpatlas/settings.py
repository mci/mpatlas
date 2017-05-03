# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
SITE_PATH = os.path.dirname(PROJECT_PATH)

# Django settings for mpatlas project.
DEBUG = False

# Override DEBUG with local_settings.py value right away.  We override all other global
# settings with local_settings.py values at the end of this file.
try:
    from local_settings import DEBUG
except ImportError:
    pass

# TEMPLATE_DEBUG = DEBUG

# Use safelogging from https://github.com/litchfield/django-safelogging
# Rate limits error log emails and suppresses disallowed hosts warnings
try:
    from safelogging.settings import *
except:
    pass

ADMINS = (
    # ('Russell Moffitt', 'Russell.Moffitt@marine-conservation.org'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.mpatlas.org', '54.68.154.94', 'localhost', '127.0.0.1']

CORS_ORIGIN_ALLOW_ALL = True
# CORS_URLS_REGEX = r'^.*$'

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
LANGUAGES = [
    ('en-us', 'English'),
]

# Site 2 is dev.mpatlas.org, 1 is mpatlas.org
SITE_ID = 1 if DEBUG else 1

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
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
#    'django.contrib.staticfiles.finders.LegacyAppDirectoriesFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_URL = '/users/login/'
#LOGIN_REDIRECT_URL = '/users/profile/'
LOGIN_REDIRECT_URL = '/explore/'

# BEGIN social_auth settings
AUTHENTICATION_BACKENDS = (
    # 'social_auth.backends.facebook.FacebookBackend',
    # 'social_auth.backends.google.GoogleOAuthBackend',
    # 'social_auth.backends.google.GoogleOAuth2Backend',
    # 'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend',
)

FACEBOOK_APP_ID     = '314437775301695'
FACEBOOK_API_SECRET = 'd9081d03e65543fd38ada066768a5f9e'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

LOGIN_URL = '/users/login/'
#LOGIN_REDIRECT_URL = '/users/profile/'
#LOGIN_REDIRECT_URL = '/explore/'
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/another-login-url/'
## SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/mpa/sites/'
# SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
# SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'
#SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'
## SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
## SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

## SOCIAL_AUTH_DEFAULT_USERNAME = 'mpatlas_socialauth_user'
# END Social_Auth settings

MIDDLEWARE_CLASSES = (
    # Uncomment to enable caching with memcached
    'django.middleware.cache.UpdateCacheMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',

    # Uncomment to enable caching with memcached
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'mpatlas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            os.path.join(PROJECT_PATH, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                # 'social_auth.context_processors.social_auth_by_name_backends',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ],
        },
    },
]

# # List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )

# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.contrib.auth.context_processors.auth',
#     'django.core.context_processors.debug',
#     'django.core.context_processors.i18n',
#     'django.core.context_processors.media',
#     'django.core.context_processors.static',
#     # 'staticfiles.context_processors.static',
#     'django.contrib.messages.context_processors.messages',
#     'django.core.context_processors.request',
#     'social_auth.context_processors.social_auth_by_name_backends',
#     'sekizai.context_processors.sekizai',
#     'cms.context_processors.cms_settings',
#     'django.template.context_processors.request',
# )

# TEMPLATE_DIRS = (
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#     os.path.join(PROJECT_PATH, 'templates'),
# )

CMS_TEMPLATES = (
    ('cms_basic.html', 'Basic Page'),
    ('cms_home.html', 'Homepage'),
    ('cms_mpapedia.html', 'MPApedia Page'),
    ('v2_cms_basic.html', 'V2 Basic Page'),
    ('v2_cms_home.html', 'V2 Homepage'),
    ('v2_news.html', 'V2 News Page'),
    ('v3_base.html', 'V3 Base HTML5BP'),
    ('v3_cms_basic.html', 'V3 Basic Page'),
    ('v3_news.html', 'V3 News Page'),
)

ALDRYN_STYLE_CLASS_NAMES = (
    ('container', _('bootstrap container')),
    ('container-fluid', _('bootstrap fluid container')),
)

# These settings override djangocms_text_ckeditor toolbar settings
# Disable server-side html sanitization via html5lib, it's removing too much right now
TEXT_HTML_SANITIZE = False
CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'toolbar': 'CMS',
    'skin': 'moono',
    'toolbarCanCollapse': False,
    'toolbar_CMS': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        ['HorizontalRule'],
        { 'name': 'links', 'items': [ 'Link', 'Unlink', 'Anchor' ] },
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        ['Source']
    ],
    'stylesSet': 'default:/static/js/addons/ckeditor.wysiwyg.js',
    'contentsCss': ['/static/css/main.css'],
}

#CKEditor
CKEDITOR_UPLOAD_PATH = 'media-uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Complete',
        # 'toolbar': 'Full',
        'toolbar_Complete': [
            ['Source', '-', 'Preview'], ['Paste', 'Paste as plain text'],
        ],

        'toolbar_Complete': [
            { 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ], 'items': [ 'Source', '-', 'Preview'] },
            { 'name': 'clipboard', 'groups': [ 'clipboard', 'undo' ], 'items': ['Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
            { 'name': 'editing', 'groups': [ 'find', 'selection', 'spellchecker' ], 'items': ['Scayt' ] },
            { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ], 'items': [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ] },
            { 'name': 'paragraph', 'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ], 'items': [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] },
            { 'name': 'links', 'items': [ 'Link', 'Unlink', 'Anchor' ] },
            { 'name': 'insert', 'items': [ 'Image', 'Table', 'HorizontalRule', 'SpecialChar', 'Iframe' ] },
            '/',
            { 'name': 'styles', 'items': [ 'Styles', 'Format', 'FontSize' ] },
            { 'name': 'colors', 'items': [ 'TextColor', 'BGColor' ] },
            { 'name': 'tools', 'items': [ 'Maximize', 'ShowBlocks' ] },
            { 'name': 'others', 'items': [ '-' ] },
        ],
        'height': 300,
        'width': '100%',
        'extraPlugins': 'image2',
        'removePlugins': 'stylesheetparser',
        'stylesSet': 'default:/static/js/addons/ckeditor.wysiwyg.js',
        'contentsCss': ['/static/css/main.css'],
    },
    'awesome_ckeditor': {
        'toolbar': 'Basic',
        'stylesSet': 'default:/static/js/addons/ckeditor.wysiwyg.js',
        'contentsCss': ['/static/css/main.css'],
    },
}

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

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
    'easy_thumbnails.processors.background',
)

THUMBNAIL_HIGH_RESOLUTION = True # for retina support

# django-filer and ckeditor integration
TEXT_SAVE_IMAGE_FUNCTION='cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'

FILER_IS_PUBLIC_DEFAULT = True
FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True

MIGRATION_MODULES = {
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages', # to enable messages framework (see :ref:`Enable messages <enable-messages>`)
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 'staticfiles',

    # 'debug_toolbar',
    
    'django_extensions',
    # 'storages',
    # 'south',  # Only needed for Django < 1.7
    'django.contrib.gis',
    'corsheaders',

    'filer',
    'easy_thumbnails',

    'cms',  # django CMS itself
    'mptt',  # utilities for implementing a tree
    'treebeard',
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for javascript and css management
    'djangocms_history',
    'reversion',

    'djangocms_attributes_field',
    
    # 'sorl.thumbnail',
    # 'django_notify',
    # 'wiki',
    # 'wiki.plugins.attachments',
    # 'wiki.plugins.notifications',
    # 'wiki.plugins.images',
    # 'wiki.plugins.macros',
    # 'wiki.plugins.links',
    # 'wiki.plugins.help',
    # # 'wiki.plugins.haystack',

    'aldryn_style',
    'aldryn_bootstrap3',

    'bootstrap_layout',

    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_link',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',

    # 'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    # 'djangocms_picture',
    'djangocms_teaser',
    # 'djangocms_video',
    'djangocms_link',
    'djangocms_snippet',
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry

    # Plaintext Plugin
    'cmsplugin_plaintext',

    #'tinymce',
    'ckeditor',
    'ckeditor_uploader',
    
    'django_countries',
    
    # User accounts and registration
    # 'social_auth',
    'accounts',

    # Tagging/Categories
    'taggit',
    'category',
    
    # Spatial data
    'world',
    'wdpa',
    'usmpa',
    'mpa',
    'spatialdata',
    'campaign',

    'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
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

