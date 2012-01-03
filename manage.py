#!/usr/bin/env env/bin/python
from django.core import management
import sys
import os


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manticore.settings.testing')
    #sys.path.insert(0, os.path.dirname(__file__))
    management.execute_from_command_line()
