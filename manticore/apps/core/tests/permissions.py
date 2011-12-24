from django.test import TestCase, Client

from ..utils import reverse
from ..models import Category
from .utils import create_user, assert_no_errors, assert_form_error, FakeFile

class PermissionTest(TestCase):
    def setUp(self):
        super(PermissionTest, self).setUp()
        self.cl = Client()
        Category.objects.get_or_create(title='First')

    def login(self, user):
        self.cl.login(username=user.username, password='test')

    def get(self, view):
        if isinstance(view, tuple):
            view, args, kwargs = view
        else:
            args, kwargs = (), {}

        url = reverse(view, *args, **kwargs)
        return self.cl.get(url)

    def post(self, view, data):
        if isinstance(view, tuple):
            view, args, kwargs = view
        else:
            args, kwargs = (), {}

        url = reverse(view, *args, **kwargs)
        return self.cl.post(url, data)

    def test_user_own_workbench_he_created(self):
        art = create_user('art')
        self.assertEqual(0, art.workbenches.count())

        self.login(art)
        result = self.post(
            'workbench-add',
            dict(
                title='test workbench',
                category=1,
            )
        )
        assert_no_errors(result)
        self.assertRedirects(result, reverse('workbench', pk=1))
        self.assertEqual(1, art.workbenches.count())

    def test_workbench_can_be_updated_only_by_owner(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        self.login(art)
        result = self.post(
            'workbench-add',
            dict(
                title='test workbench',
                category=1,
            )
        )
        edit_url = ('workbench-edit', (), {'pk': art.workbenches.all()[0].pk})

        # and updates it's title
        result = self.post(
            edit_url,
            dict(
                title='another title',
                category=1,
            )
        )
        self.assertEqual('another title', art.workbenches.all()[0].title)


        # then Peter tries to modify Art's workbench
        self.login(peter)

        # and updates it's title
        result = self.post(
            edit_url,
            dict(
                title='hacked title',
                category=1,
            )
        )
        # he should receive an 403 (access denied) error
        self.assertEqual(403, result.status_code)
        # and workbench's title should remain the same
        self.assertEqual('another title', art.workbenches.all()[0].title)

        # Peter even can't see the edit page
        self.assertEqual(403, self.get(edit_url).status_code)

    def test_nail_can_be_uploaded_only_to_workbench_owned_by_user(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        self.login(art)
        result = self.post(
            'workbench-add',
            dict(
                title='test workbench',
                category=1,
            )
        )
        workbench = art.workbenches.all()[0]

        # and uploads a nail
        result = self.post(
            'nail-add',
            dict(
                workbench=workbench.pk,
                description='test nail',
                original=FakeFile(),
            )
        )
        assert_no_errors(result)
        self.assertEqual(1, workbench.nails.count())

        # and now Peter tries to upload a nail into Art's workbench
        self.login(peter)

        result = self.post(
            'nail-add',
            dict(
                workbench=workbench.pk,
                description='test nail',
                original=FakeFile(),
            )
        )
        # he should receive an 403 (access denied) error
        assert_form_error(result, 'workbench', 'Select a valid choice')
        # and workbench's title should remain the same
        self.assertEqual(1, workbench.nails.count())

    def test_nail_upload_page_allows_to_choose_only_owned_workbenches(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        self.login(art)
        self.post(
            'workbench-add',
            dict(
                title='ArtWorkbench',
                category=1,
            )
        )
        # Peter creates a workbench too
        self.login(peter)
        self.post(
            'workbench-add',
            dict(
                title='PeterWorkbench',
                category=1,
            )
        )

        # now Peter opens nail upload page
        response = self.get('nail-add')
        self.assertContains(response, 'PeterWorkbench')
        self.assertNotContains(response, 'ArtWorkbench')

    def test_workbench_or_nail_can_not_be_created_by_anonymous(self):
        self.assertEqual(403, self.get('workbench-add').status_code)
        self.assertEqual(403, self.get('nail-add').status_code)

