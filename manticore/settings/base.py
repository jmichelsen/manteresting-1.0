# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import re
import os.path
import posixpath

from manticore.apps.core.extlinks import ExtlinksBlankMiddleware
from manticore.apps.core.utils import reverse
from django.template.defaultfilters import slugify

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

INTERNAL_IPS = [
    '127.0.0.1',
]

ADMINS = [
    # ('Admin', 'admin@manteresting.com'),
]

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'manteresting',                       # Or path to database file if using sqlite3.
        'USER': 'manteresting',                             # Not used with sqlite3.
        'PASSWORD': 'manteresting',                         # Not used with sqlite3.
        'HOST': '127.0.0.1',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: '/home/media/media.lawrence.com/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: 'http://media.lawrence.com', 'http://example.com/media/'
MEDIA_URL = '/site_media/media/'

# Absolute path to the directory that holds static files like app media.
# Example: '/home/media/media.lawrence.com/apps/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'site_media', 'static')

# URL that handles the static files like app media.
# Example: 'http://media.lawrence.com'
STATIC_URL = '/site_media/static/'

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
    MEDIA_ROOT,
]

STATICFILES_FINDERS = [
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder',
    'staticfiles.finders.LegacyAppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: 'http://foo.com/media/', '/media/'.
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, 'admin/')

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = 'cache'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q-j311$ugovqxv(3f%5=s)iy7%on24j3(q_twm88%#e+l&l*$j'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_openid.consumer.SessionConsumer',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pinax.apps.account.middleware.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'pinax.middleware.security.HideSensistiveFieldsMiddleware',
    'manticore.apps.core.extlinks.ExtlinksBlankMiddleware',
]

ROOT_URLCONF = 'manticore.urls'

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, 'templates'),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    
    'staticfiles.context_processors.static',
    
    'pinax.core.context_processors.pinax_settings',
    
    'pinax.apps.account.context_processors.account',
    
    'notification.context_processors.notification',
    'announcements.context_processors.site_wide_announcements',
    'social_auth.context_processors.social_auth_by_type_backends',
    'manticore.apps.core.context_processors.settings',
]

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',

    'pinax.templatetags',

    # theme
    'pinax_theme_bootstrap',

    # external
    'notification', # must be first
    'staticfiles',
    'compressor',
    'mailer',
    'django_openid',
    'timezones',
    'emailconfirmation',
    'announcements',
    'pagination',
    'idios',
    'metron',
    'social_auth',
    'imagekit',
    'south',
    'phileo',
    'dialogos',
    'follow',
    'haystack',
    'endless_pagination',

    # Pinax
    'pinax.apps.account',
    'pinax.apps.signup_codes',

    # project
    'manticore.apps.about',
    'manticore.apps.profiles',
    'manticore.apps.core',
]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, 'fixtures'),
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

EMAIL_BACKEND = 'mailer.backend.DbBackend'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: reverse('user', slug=o.username),
}

AUTH_PROFILE_MODULE = 'profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = True 
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = True

AUTHENTICATION_BACKENDS = [
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'pinax.apps.account.auth_backends.AuthenticationBackend',
]

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter', 'facebook')
SOCIAL_AUTH_USERNAME_FIXER = lambda u: slugify(u)
SOCIAL_AUTH_EXTRA_DATA = False

LOGIN_URL = '/account/login/' # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = 'what_next'
LOGOUT_REDIRECT_URLNAME = 'home'

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

PHILEO_LIKABLE_MODELS = [
    'core.Nail',
]

# Search settings
HAYSTACK_SITECONF = 'manticore.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'search_index')

# Endless scrolling settings.
# See http://django-endless-pagination.readthedocs.org/en/latest/customization.html#settings
ENDLESS_PAGINATION_PER_PAGE = 40
ENDLESS_PAGINATION_LOADING = """<img src="http://manteresting.com/site_media/static/loading.gif" alt="loading" />"""

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass

for name in ('INSTALLED_APPS',):
    locals()[name] = locals().get('patch_' + name.lower(), lambda x: x)(locals().get(name))

