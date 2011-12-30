from ..utils import reverse
from ..models import Category
from .utils import create_user, assert_no_errors, assert_form_error, TestCase

class PermissionTest(TestCase):
    def setUp(self):
        super(PermissionTest, self).setUp()
        Category.objects.get_or_create(title='First')

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
        workbench = self.create_workbench(art)
        edit_url = ('workbench-edit', (), {'pk': workbench.pk})

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
        workbench = self.create_workbench(art)
        # and uploads a nail
        self.create_nail(workbench)
        self.assertEqual(1, workbench.nails.count())

        # and now Peter tries to upload a nail into Art's workbench
        response = self.create_nail(workbench, as_user=peter)
        # he should receive an 403 (access denied) error
        assert_form_error(response, 'workbench', 'Select a valid choice')
        # and workbench's title should remain the same
        self.assertEqual(1, workbench.nails.count())

    def test_nail_upload_page_allows_to_choose_only_owned_workbenches(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        self.create_workbench(art, title='ArtWorkbench')
        # Peter creates a workbench too
        self.create_workbench(peter, title='PeterWorkbench')

        # now Peter opens nail upload page
        self.login(peter)
        response = self.get('nail-add')
        self.assertContains(response, 'PeterWorkbench')
        self.assertNotContains(response, 'ArtWorkbench')

    def test_workbench_or_nail_can_not_be_created_by_anonymous(self):
        self.assertEqual(403, self.get('workbench-add').status_code)
        self.assertEqual(403, self.get('nail-add').status_code)

    def test_delete_nail(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        workbench = self.create_workbench(art)
        # and uploads a nail
        nail = self.create_nail(workbench)

        delete_url = ('nail-delete', (), dict(pk=nail.pk))

        # Now Peter tries to delete Art's nail
        self.login(peter)
        response = self.post(delete_url)
        self.assertEqual(403, response.status_code)
        # but he fails
        self.assertEqual(1, workbench.nails.count())

        # Now Art deletes his nail
        self.login(art)
        response = self.post(delete_url)
        assert_no_errors(response)
        # he success
        self.assertEqual(0, workbench.nails.count())

    def test_nail_can_be_updated_only_by_workbench_owner(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        workbench = self.create_workbench(art)
        # and uploads a nail
        nail = self.create_nail(workbench)

        # Now Peter tries to change Art's nail
        self.login(peter)
        result = self.post(
            ('nail-edit', (), dict(pk=nail.pk)),
            dict(description='hacked')
        )
        # he should receive an 403 (access denied) error
        self.assertEqual(403, result.status_code)
        # and nail's description should remain the same
        self.assertEqual('test nail', workbench.nails.all()[0].description)

    def test_delete_workbench(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        workbench = self.create_workbench(art)

        # Now Peter tries to delete Art's workbench
        self.login(peter)
        result = self.post(
            ('workbench-delete', (), dict(pk=workbench.pk))
        )
        # but he fails
        self.assertEqual(403, result.status_code)
        self.assertEqual(1, art.workbenches.count())

        # Now Art deletes his nail
        self.login(art)
        result = self.post(
            ('workbench-delete', (), dict(pk=workbench.pk))
        )
        assert_no_errors(result)
        # but he success
        self.assertEqual(0, art.workbenches.count())

    def test_nail_edit_page_allows_to_choose_only_owned_workbenches(self):
        art = create_user('art')
        peter = create_user('peter')

        # Art creates a workbench
        arts_workbench = self.create_workbench(art, title='ArtWorkbench')

        # Peter creates a workbench too
        peters_workbench = self.create_workbench(peter, title='PeterWorkbench')
        nail = self.create_nail(peters_workbench)

        # now Peter opens nail upload page
        response = self.get(('nail-edit', (), dict(pk=nail.pk)))
        self.assertContains(response, peters_workbench.title)
        self.assertNotContains(response, arts_workbench.title)
