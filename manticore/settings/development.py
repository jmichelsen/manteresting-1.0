from manticore.settings.base import *

TWITTER_CONSUMER_KEY         = 'vq0kbj6Mig8I8xqaExLWVg'
TWITTER_CONSUMER_SECRET      = 'Z0UGeJFK1nOTC7cwbaVDMV1cfpoTpOYmryPPif90'
FACEBOOK_APP_ID              = '103290089779983'
FACEBOOK_API_SECRET          = '75fdcd8649db32303eb403887d7e85e4'

INSTALLED_APPS.append('django_extensions')

# django-debug-toolbar settings
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

DEBUG_TOOLBAR_CONFIG = dict(
    SHOW_TOOLBAR_CALLBACK=lambda request: DEBUG,
    HIDE_DJANGO_SQL=False,
    INTERCEPT_REDIRECTS=False,
)

