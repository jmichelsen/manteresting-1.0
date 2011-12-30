from ..models import Category
from .utils import TestCase, create_user, assert_no_errors, assert_form_error, FakeFile

class PinningTest(TestCase):
    def setUp(self):
        super(PinningTest, self).setUp()
        Category.objects.get_or_create(title='First')

        self.art = create_user('art')
        self.peter = create_user('peter')

        # Art has two workbenches
        workbench = self.create_workbench(self.art, title='first workbench')
        self.create_workbench(self.art, title='second workbench')
        # and uploads a nail
        self.create_nail(workbench)

        # Peter creates workbench too
        self.create_workbench(self.peter, title='another workbench')

    def test_nail_repin_page_contains_original_description_and_right_workbenches(self):
        # Peter tries to repin a nail from Art's workbench
        self.login(self.peter)

        self.assertEqual(0, self.peter.workbenches.all()[0].nails.count())

        nail = self.art.workbenches.all()[0].nails.all()[0]
        response = self.get(
            ('nail-repin', (), dict(pk=nail.pk)),
        )
        self.assertContains(response, 'test nail')
        self.assertContains(response, 'another workbench')
        self.assertContains(response, 'Repin')

        self.assertNotContains(response, 'Upload')
        self.assertNotContains(response, 'first workbench')
        self.assertNotContains(response, 'second workbench')

    def test_nail_repin(self):
        # Peter tries to repin a nail from Art's workbench
        self.login(self.peter)

        self.assertEqual(0, self.peter.workbenches.all()[0].nails.count())

        original_nail = self.art.workbenches.all()[0].nails.all()[0]

        response = self.post(
            ('nail-repin', (), dict(pk=original_nail.pk)),
            dict(
                workbench=self.peter.workbenches.all()[0].pk,
                description='some description',
            )
        )
        assert_no_errors(response)
        self.assertEqual(1, self.peter.workbenches.all()[0].nails.count())

        new_nail = self.peter.workbenches.all()[0].nails.all()[0]
        self.assertEqual('some description', new_nail.description)

        self.assertEqual([new_nail], list(original_nail.clones.all()))
        self.assertEqual(original_nail, new_nail.cloned_from)

        # check that page opens without errors
        response = self.get(('nail', (), dict(pk=new_nail.pk)))
        self.assertEqual(200, response.status_code)

    def test_user_cant_repin_into_others_workbench(self):
        first_workbench, second_workbench = list(self.art.workbenches.all())

        self.assertEqual(1, first_workbench.nails.count())
        self.assertEqual(0, second_workbench.nails.count())

        original_nail = first_workbench.nails.all()[0]

        # Peter tries to repin a nail from Art's workbench into another
        # Art's workbench
        self.login(self.peter)

        response = self.post(
            ('nail-repin', (), dict(pk=original_nail.pk)),
            dict(
                workbench=second_workbench.pk,
                description='some description',
            )
        )
        # he should receive an error or form validation
        assert_form_error(response, 'workbench', 'Select a valid choice')

        # and nothing changed
        self.assertEqual(1, first_workbench.nails.count())
        self.assertEqual(0, second_workbench.nails.count())

    def test_dont_delete_clone_when_original_deleted(self):
        original_nail = self.art.workbenches.all()[0].nails.all()[0]

        # Peter repins a nail from Art's workbench
        self.login(self.peter)
        self.post(
            ('nail-repin', (), dict(pk=original_nail.pk)),
            dict(
                workbench=self.peter.workbenches.all()[0].pk,
                description='some description',
            )
        )

        clone = self.peter.workbenches.all()[0].nails.all()[0]
        self.assertEqual(original_nail, clone.cloned_from)

        # and now original nail got deleted
        original_nail.delete()

        self.assertEqual(1, self.peter.workbenches.all()[0].nails.count())
        clone = self.peter.workbenches.all()[0].nails.all()[0]
        self.assertEqual(None, clone.cloned_from)

