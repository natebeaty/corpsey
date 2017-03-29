import os

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

ALLOWED_HOSTS = []

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
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

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

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'corpsey', 'static'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'corpsey.urls'
LOGIN_URL = '/user/login/'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'corpsey.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'corpsey', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'corpsey.context_processors.analytics',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'easy_thumbnails',
    'django_cleanup',
    'mptt',
    'treeadmin',
    'corpsey.apps.comics',
    'corpsey.apps.artists',
    'flatpages_x',
    'markitup',
    'clear_cache',
    'cronjobs',
]

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

# Various app settings
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

MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_SKIN = 'markitup/skins/simple'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
FLATPAGES_X_PARSER= ["flatpages_x.markdown_parser.parse", {}]

# How many contributions can follow a comic
MAX_COMIC_CHILDREN = 3

# Override these in settings_production.py & settings_local.py
GOOGLE_ANALYTICS_KEY = ''

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'hal@trubble.club'
SERVER_EMAIL = 'hal@trubble.club'

SECRET_KEY = ''
DKIM_DOMAIN = ''
DKIM_SELECTOR = ''
DKIM_PRIVATE_KEY = ''

# Import settings information based on node
STAGING_HOST = "corpsey-staging"
PRODUCTION_HOST = "web591.webfaction.com"

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
