from django.conf import settings as django_settings
import logging

def settings(request):
    return {
        'settings': django_settings
    }
