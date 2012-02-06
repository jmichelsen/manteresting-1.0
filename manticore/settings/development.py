from manticore.settings.base import *

TWITTER_CONSUMER_KEY         = 'vq0kbj6Mig8I8xqaExLWVg'
TWITTER_CONSUMER_SECRET      = 'Z0UGeJFK1nOTC7cwbaVDMV1cfpoTpOYmryPPif90'
FACEBOOK_APP_ID              = '103290089779983'
FACEBOOK_API_SECRET          = '75fdcd8649db32303eb403887d7e85e4'

INSTALLED_APPS.append('django_extensions')

# django-debug-toolbar settings
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',

    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',

    #'debug_toolbar.panels.sql.SQLDebugPanel',
    #'debug_toolbar.panels.profiling.ProfilingDebugPanel',
)

DEBUG_TOOLBAR_CONFIG = dict(
    SHOW_TOOLBAR_CALLBACK=lambda request: DEBUG,
    HIDE_DJANGO_SQL=False,
    INTERCEPT_REDIRECTS=False,
)

