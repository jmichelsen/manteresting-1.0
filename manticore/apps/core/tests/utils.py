import os.path
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


def FakeFile():
    """File to test image uploads"""
    return open(
        os.path.join(
            os.path.dirname(__file__),
            '../../../site_media/static/images/openid-icon.png'
        ),
        'rb'
    )

