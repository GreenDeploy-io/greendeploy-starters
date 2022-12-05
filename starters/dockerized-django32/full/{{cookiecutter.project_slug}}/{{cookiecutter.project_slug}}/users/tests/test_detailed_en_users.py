from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import lorem_ipsum
from eno_a3_django.users.models import EnProfile
from eno_a3_django.users.tests.factories import UserFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class TestCase(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name="ENO")
        self.user = UserFactory(groups=[self.group])
        self.url = reverse("apiv1:detailed_en_users-list")
        self.detail_url = reverse("apiv1:detailed_en_users-detail", args=(self.user.pk,))

    def test_forbidden(self):
        """
        Disallow delete
        """
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create(self):
        """
        Successfully create new user
        """
        self.client.force_authenticate(self.user)
        data = {
            "en_profile": {
                "signum": lorem_ipsum.words(1),
                "org_unit_short_name": lorem_ipsum.words(1),
            },
            "name": lorem_ipsum.words(1),
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": "test@example.com",
            "groups": [self.group.id],
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(EnProfile.objects.count(), 1)
        user = User.objects.last()
        self.assertEqual(user.username, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.en_profile.signum, data["en_profile"]["signum"])
        self.assertEqual(
            user.en_profile.org_unit_short_name, data["en_profile"]["org_unit_short_name"]
        )

    def test_create_fail(self):
        """
        User passes invalid data and gets errors during new user creating
        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "en_profile": ["This field is required."],
                "groups": ["This field is required."],
                "username": ["This field is required."],
            },
        )

    def test_update(self):
        """
        User successfully update user
        """
        self.client.force_authenticate(self.user)
        group = Group.objects.create(name=lorem_ipsum.words(1))
        data = {
            "en_profile": {
                "signum": lorem_ipsum.words(1),
                "org_unit_short_name": lorem_ipsum.words(1),
            },
            "name": lorem_ipsum.words(1),
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": "test@example.com",
            "groups": [self.group.id, group.id],
        }

        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, data["username"])
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        self.assertEqual(self.user.en_profile.signum, data["en_profile"]["signum"])
        self.assertEqual(
            self.user.en_profile.org_unit_short_name, data["en_profile"]["org_unit_short_name"]
        )

    def test_update_fail(self):
        """
        User passes invalid data and gets errors during user updating
        """
        self.client.force_authenticate(self.user)
        data = {"email": "test"}

        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["Enter a valid email address."]})
