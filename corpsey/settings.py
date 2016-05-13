# Django settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Nate Beaty', 'nate@clixel.com'),
)

MANAGERS = (
    ('Nate Beaty', 'nate@clixel.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'corpsey_dev',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/natebeaty/webapps/corpsey_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/natebeaty/webapps/django14_static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/natebeaty/webapps/django15/corpsey/corpsey/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'corpsey.urls'
LOGIN_URL = '/user/login/'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'corpsey.wsgi.application'

ICANHAZ_DIRS = (
    '/home/natebeaty/webapps/django15/corpsey/corpsey/templates/icanhaz',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/natebeaty/webapps/django15/corpsey/corpsey/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'corpsey.context_processors.analytics',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'easy_thumbnails',
    'django_cleanup',
    'mptt',
    'treeadmin',
    'south',
    'corpsey.apps.comics',
    'corpsey.apps.artists',
    'dajaxice',
    'dajax',
    'icanhaz',
    'flatpages_x',
    'markitup',
    'clear_cache',
    'cronjobs',
    'compressor',
)

MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_SKIN = 'markitup/skins/simple'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
FLATPAGES_X_PARSER= ["flatpages_x.markdown_parser.parse", {}]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/natebeaty/memcached.sock',
    }
}


# override these in settings_production.py & settings_local.py
GOOGLE_ANALYTICS_KEY = ''

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'hal@trubbleclub.com'
SERVER_EMAIL = 'hal@trubbleclub.com'

SECRET_KEY = ''
DKIM_DOMAIN = ''
DKIM_SELECTOR = ''
DKIM_PRIVATE_KEY = ''

GRAPPELLI_ADMIN_TITLE = 'Infinitely Corpsey'
THUMBNAIL_ALIASES = {
    '': {
        'midsize': {'size': (330, 330), 'crop': True, 'quality': 90},
        'midsize_hd': {'size': (660, 660), 'crop': True, 'quality': 85},
        'tree': {'size': (100, 100), 'crop': True, 'quality': 75},
    },
}
THUMBNAIL_BASEDIR = 'thumbs'
THUMBNAIL_DEBUG = True
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)

MAX_COMIC_CHILDREN = 3

# Import settings information based on node
STAGING_HOST = "corpsey-staging"
PRODUCTION_HOST = "web376.webfaction.com"

from platform import node

if node() == STAGING_HOST:
    from settings_staging import *
elif node() == PRODUCTION_HOST:
    from settings_production import *
else:
    try:
        from settings_local import *
    except ImportError:
        pass
