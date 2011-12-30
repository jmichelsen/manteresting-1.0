import os.path

from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase, Client
from nose.tools import eq_

from ..utils import reverse


def create_user(username):
    u = User.objects.create_user(username, username + '@dev.manticore.com', 'test')
    return u

def assert_no_errors(response):
    try:
        errors = response.context and response.context['form'].errors or None
    except KeyError:
        errors = None
    eq_(None, errors)


def assert_form_error(response, field, error):
    errors = response.context and response.context['form'].errors or []

    if not errors:
        raise AssertionEror('no form errors')

    if field not in errors:
        raise AssertionEror('no form errors for "%s" field' % field)

    if error.lower() not in u' '.join(errors[field]).lower():
        raise AssertionEror('no error "%s" for "%s" field' % (error, field))


def FakeFile():
    """File to test image uploads"""
    return open(
        os.path.join(
            os.path.dirname(__file__),
            '../../../site_media/static/images/openid-icon.png'
        ),
        'rb'
    )


class TestCase(DjangoTestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.cl = Client()

    def login(self, user):
        self.cl.login(username=user.username, password='test')

    def get(self, view):
        if isinstance(view, tuple):
            view, args, kwargs = view
        else:
            args, kwargs = (), {}

        url = reverse(view, *args, **kwargs)
        return self.cl.get(url)

    def post(self, view, data=None):
        if isinstance(view, tuple):
            view, args, kwargs = view
        else:
            args, kwargs = (), {}

        url = reverse(view, *args, **kwargs)
        return self.cl.post(url, {} if data is None else data)

    def create_nail(self, workbench, description='test nail', as_user=None):
        if as_user is not None:
            self.login(as_user)
        else:
            self.login(workbench.user)

        response = self.post(
            'nail-add',
            dict(
                workbench=workbench.pk,
                description=description,
                original=FakeFile(),
            )
        )
        if as_user is None or as_user == workbench.user:
            assert_no_errors(response)
            return workbench.nails.all().order_by('-id')[0]

        return response

    def create_workbench(self, owner, title='test workbench'):
        self.login(owner)
        response = self.post(
            'workbench-add',
            dict(
                title=title,
                category=1,
            )
        )
        assert_no_errors(response)
        return owner.workbenches.all().order_by('-id')[0]

