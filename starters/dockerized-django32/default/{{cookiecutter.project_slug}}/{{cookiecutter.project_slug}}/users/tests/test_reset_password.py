from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from eno_a3_django.users.tests.factories import RoleFactory, UserFactory
from organizations.models import Domain
from organizations.tests.factories import DomainFactory, OrganizationFactory


class ResetPasswordTestCase(APITestCase):
    """
    eno_a3_django.users.tests.test_reset_password.ResetPasswordTestCase --keepdb
    """

    def setUp(self):
        self.organization = OrganizationFactory(domain="localhost", name="ENP")
        self.domain2 = DomainFactory(organization=self.organization)
        self.totalboq_domain = DomainFactory(
            organization=self.organization, name="ph-sea.thetotalboq.com"
        )
        self.user = UserFactory()
        self.url = reverse("rest_password_reset")

        # setup the right roles and people
        roles = [{"name": "ENO"}, {"name": "Admin", "path": "ENO.Admin"}]

        for role in roles:
            RoleFactory(**role)

        self.eno_group = Group.objects.get(name="ENO")
        self.admin_group = Group.objects.get(name="Admin")
        self.admin_user = UserFactory(groups=[self.eno_group, self.admin_group])

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_rest_password(self):
        """
        User resets password successfully
        """
        data = {"email": self.user.email}
        # User send request from the domain2
        response = self.client.post(
            self.url, data, HTTP_HOST="{}:8000".format(self.domain2)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"detail": "Password reset e-mail has been sent."}
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, f"[{self.domain2.name}] Password Reset E-mail"
        )

        path = reverse(
            "account_reset_password_from_key",
            kwargs=dict(
                uidb36=user_pk_to_url_str(self.user),
                key=EmailAwarePasswordResetTokenGenerator().make_token(self.user),
            ),
        )
        self.assertTrue(f"http://{self.domain2}:8000{path}" in mail.outbox[0].body)
        self.assertTrue(self.domain2.name in mail.outbox[0].body)
        self.assertTrue(self.domain2.organization.name in mail.outbox[0].body)

        # User send request from the domain1
        domain1 = Domain.objects.exclude(pk=self.domain2.pk).first()
        response = self.client.post(
            self.url, data, HTTP_HOST="{}:8000".format(domain1.name)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"detail": "Password reset e-mail has been sent."}
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(
            mail.outbox[1].subject, f"[{domain1.name}] Password Reset E-mail"
        )
        self.assertTrue(f"http://{domain1}:8000{path}" in mail.outbox[1].body)
        self.assertTrue(domain1.name in mail.outbox[1].body)
        self.assertTrue(domain1.organization.name in mail.outbox[1].body)

        # User send request from the domain which not exists
        response = self.client.post(self.url, data, HTTP_HOST="testserver")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"detail": "Password reset e-mail has been sent."}
        )
        self.assertEqual(len(mail.outbox), 3)
        site = Site.objects.first()
        self.assertEqual(mail.outbox[2].subject, f"[{site.name}] Password Reset E-mail")
        self.assertTrue(f"http://testserver{path}" in mail.outbox[2].body)

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_rest_password_for_vendor(self):
        """
        Admin resets password successfully for vendor for specific domain
        """
        self.client.force_authenticate(self.admin_user)
        data = {"email": self.user.email, "domain": "ph-sea.thetotalboq.com"}
        url = reverse("apiv1:vendor_reset_password-reset-password")
        response = self.client.post(url, data, HTTP_HOST="testserver")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"detail": "Password reset e-mail has been sent."}
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(data["domain"] in mail.outbox[0].body)
