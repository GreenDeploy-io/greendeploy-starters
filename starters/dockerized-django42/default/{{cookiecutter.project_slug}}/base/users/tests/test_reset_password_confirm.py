from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from eno_a3_django.users.tests.factories import UserFactory, TEST_USER_PASSWORD


class ResetPasswordConfirmTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('rest_password_reset_confirm')

    def test_rest_password_confirm(self):
        """
        User resets password successfully
        """
        data = {
            'new_password1': TEST_USER_PASSWORD,
            'new_password2': TEST_USER_PASSWORD,
            'uid': user_pk_to_url_str(self.user),
            'token': default_token_generator.make_token(self.user)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': 'Password has been reset with the new password.'})

    def test_rest_password_confirm_invalid_token(self):
        """
        User uses incorrect reset password token and gets an error
        """
        data = {
            'new_password1': TEST_USER_PASSWORD,
            'new_password2': TEST_USER_PASSWORD,
            'uid': user_pk_to_url_str(self.user),
            'token': 'test'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'token': ['Invalid value']})

    def test_rest_password_confirm_invalid_uid(self):
        """
        User uses incorrect reset password uid and gets an error
        """
        data = {
            'new_password1': TEST_USER_PASSWORD,
            'new_password2': TEST_USER_PASSWORD,
            'uid': 'test',
            'token': default_token_generator.make_token(self.user)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'uid': ['Invalid value']})

    def test_rest_password_confirm_invalid_password(self):
        """
        User uses invalid password during reset password and gets an error
        """
        data = {
            'new_password1': TEST_USER_PASSWORD,
            'new_password2': 'test',
            'uid': user_pk_to_url_str(self.user),
            'token': default_token_generator.make_token(self.user)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'new_password2': ['The two password fields didn\'t match.']})
