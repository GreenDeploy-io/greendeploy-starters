from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from stream_django.client import stream_client

from eno_a3_django.users.tests.factories import TEST_USER_PASSWORD, UserFactory


class LoginTestCase(APITestCase):
    """
    eno_a3_django.users.tests.test_login.LoginTestCase --keepdb
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("rest_login")

    def test_login(self):
        """
        User logs in successfully
        """
        data = {"email": self.user.email, "password": TEST_USER_PASSWORD}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        feed = stream_client.feed(
            settings.STREAM_GLOBAL_FEED_NAME, settings.STREAM_GLOBAL_NOTIFICATIONS
        )
        notification_token = feed.get_readonly_token()
        self.assertEqual(
            response.json(),
            {
                "key": self.user.auth_token.key,
                "notification_token": notification_token,
                "user_id": self.user.pk,
            },
        )

    def test_login_fail(self):
        """
        User sets incorrect credentials and gets error message
        """
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"password": ["This field is required."]})

        response = self.client.post(self.url, {"password": TEST_USER_PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ['Must include "email" and "password".']},
        )
