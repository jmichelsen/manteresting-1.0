from ..models import Category
from .utils import TestCase, create_user, assert_no_errors, assert_form_error, FakeFile

class FriendFeedTest(TestCase):
    def setUp(self):
        super(FriendFeedTest, self).setUp()
        """ Here we have two users: Alex and Peter.
        Alex likes photography and has two workbenches: Landscapes and Portrets.
        Peter likes Cars and Girls.

        Each workbench contains one image.
        """
        Category.objects.get_or_create(title='First')

        self.alex = create_user('alex')
        self.peter = create_user('peter')

        self.alex_w1 = self.create_workbench(self.alex, title="Alex's workbench 1")
        self.alex_w2 = self.create_workbench(self.alex, title="Alex's workbench 2")
        self.create_nail(self.alex_w1)
        self.create_nail(self.alex_w2)

        self.peter_w1 = self.create_workbench(self.peter, title="Peter's workbench 1")
        self.peter_w2 = self.create_workbench(self.peter, title="Peter's workbench 2")
        self.create_nail(self.peter_w1)
        self.create_nail(self.peter_w2)


    def test_feeds_are_empty_by_default(self):
        # Peter tries to repin a nail from Art's workbench
        self.login(self.peter)

        self.assertEqual(0, self.alex.friendfeed.count())
        self.assertEqual(0, self.peter.friendfeed.count())

    def test_alex_get_1_if_follow_peters_workbench(self):
        self.login(self.alex)
        self.follow(self.peter_w1)
        self.assertEqual(1, self.alex.friendfeed.count())

    def test_alex_get_2_if_follow_peter(self):
        self.login(self.alex)
        self.follow(self.peter)
        self.assertEqual(2, self.alex.friendfeed.count())

    def test_alex_still_get_2_if_follow_peter_and_his_workbenches(self):
        self.login(self.alex)
        self.follow(self.peter)
        self.follow(self.peter_w1)
        self.follow(self.peter_w2)
        self.assertEqual(2, self.alex.friendfeed.count())

    def test_and_alex_still_has_2_if_he_unfollow_peters_workbenches_but_follow_peter(self):
        self.login(self.alex)
        self.follow(self.peter)
        self.follow(self.peter_w1)
        self.follow(self.peter_w2)

        self.unfollow(self.peter_w1)
        self.unfollow(self.peter_w2)
        self.assertEqual(2, self.alex.friendfeed.count())

    def test_and_alex_still_has_2_if_he_unfollow_peter_but_follows_his_workbenches(self):
        self.login(self.alex)
        self.follow(self.peter)
        self.follow(self.peter_w1)
        self.follow(self.peter_w2)

        self.unfollow(self.peter)
        self.assertEqual(2, self.alex.friendfeed.count())

    def test_alex_see_nothing_after_complete_unfollow(self):
        self.login(self.alex)
        self.follow(self.peter)
        self.follow(self.peter_w1)
        self.follow(self.peter_w2)

        self.unfollow(self.peter)
        self.unfollow(self.peter_w1)
        self.unfollow(self.peter_w2)
        self.assertEqual(0, self.alex.friendfeed.count())

    def test_if_two_users_can_follow_the_same_object(self):
        bob = create_user('bob')
        martin = create_user('martin')

        self.login(bob)
        self.follow(self.alex_w1)

        self.login(martin)
        self.follow(self.alex_w1)

        self.assertEqual(1, bob.friendfeed.count())
        self.assertEqual(1, martin.friendfeed.count())

    def follow(self, what):
        self.post(
            ('follow', (), dict(app=what._meta.app_label, model=what._meta.module_name, id=what.id)),
        )

    def unfollow(self, what):
        self.post(
            ('unfollow', (), dict(app=what._meta.app_label, model=what._meta.module_name, id=what.id)),
        )

