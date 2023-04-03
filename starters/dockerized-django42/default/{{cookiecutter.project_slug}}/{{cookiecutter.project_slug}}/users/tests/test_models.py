from test_plus.test import TestCase

from eno_a3_django.users.tests.factories import EnProfileFactory


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            "testuser",  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), "/users/testuser/")


class TestEnProfile(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.en_profile = EnProfileFactory(user=self.user)

    def test__str__(self):
        self.assertEqual(
            self.en_profile.__str__(),
            "testuser",  # This is the default username for self.make_user()
        )
