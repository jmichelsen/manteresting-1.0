from django.contrib.auth.models import User
from nose.tools import eq_

def create_user(username):
    u = User.objects.create_user(username, username + '@dev.manticore.com', 'test')
    return u

def assert_no_errors(response):
    try:
        errors = response.context and response.context['form'].errors or None
    except KeyError:
        errors = None
    eq_(None, errors)
