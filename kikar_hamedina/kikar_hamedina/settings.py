import os
from os.path import dirname, abspath, join

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

sub_path = lambda *x: os.path.join(PROJECT_ROOT, *x)

# Configuring LOGS_ROOT
LOGS_ROOT = sub_path("logs")

# Configuring DATA_ROOT
DATA_ROOT = sub_path("data")

# Configuring MEDIA_ROOT
MEDIA_ROOT = sub_path("media")

# Configuring STATIC_ROOT
STATIC_ROOT = sub_path("collected_static")

# Configurion CLASSIFICATION_DATA_ROOT for autoTag and kikartags
CLASSIFICATION_DATA_ROOT = sub_path("classification_data")

# Additional locations of static files
STATICFILES_DIRS = (
    sub_path('static'),
)

# Configuring TEMPLATE_DIRS
TEMPLATE_DIRS = sub_path("templates")

SECRET_KEY = 'yz2HiIDgrCDeHSfJSXIep3FeEQunsUhnC3P9ehGZ/KHVhLXNCZ'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.comments',
    'django.contrib.humanize',
    #Third-Party
    'rest_framework',
    'django_extensions',
    'south',
    'pagination',
    'tagging',
    'dumpdata_chunks',
    'django_pandas',
    'taggit',
    'tastypie',
    'mptt',
    'zinnia',
    'endless_pagination',
    'planet',
    'links',
    'video',
    'polymorphic',
    # 'autotag_app',
    #Ours
    'kikartags',
    'knesset',
    'mks',
    'facebook_feeds',
    'core',
    'updater',
    'persons',
    'reporting',
    'polyorg',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "planet.context_processors.context",
    "core.context_processors.generic",
    "zinnia.context_processors.version",
)

ROOT_URLCONF = 'kikar_hamedina.urls'

WSGI_APPLICATION = 'kikar_hamedina.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kikar',
        'USER': 'kikar',
        'PASSWORD': 'kikar',
        'HOST': 'localhost'
    }
}

LANGUAGE_CODE = 'he'

TIME_ZONE = 'Asia/Jerusalem'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#Django-planet settings
PLANET = {
    "USER_AGENT": "Kikar-Hamedina Planet/1.0"
}

SITE_ID = 1


#Django-taggit settings
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

LANGUAGE_COOKIE_NAME = "he"
SESSION_COOKIE_NAME = "myplanetid"


CURRENT_KNESSET_NUMBER = 20
CURRENT_ELECTED_KNESSET_NUMBER = CURRENT_KNESSET_NUMBER + 1

# In elections mode e.g. Knesset candidates are shown instead of Knesset members
IS_ELECTIONS_MODE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(asctime)s - %(message)s'
        },
    },
    'handlers': {
        'scrapeFile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'simple'
        },
        'scraping': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/scarping.log' % LOGS_ROOT,
            'maxBytes': 1024 * 1024 * 10,  # 10MB each log file
            'backupCount': 10,
            'formatter': 'simple'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['scrapeFile'],
            'propagate': True,
            'level': 'INFO',
        },
        'scraping': {
            'handlers': ['scraping'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TASTYPIE_DEFAULT_FORMATS = ['json']

try:
    from .local_settings import *
except ImportError:
    pass
