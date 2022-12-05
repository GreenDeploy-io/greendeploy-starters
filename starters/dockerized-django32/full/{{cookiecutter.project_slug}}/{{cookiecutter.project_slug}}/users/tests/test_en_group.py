from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import override_settings
from eno_a3_django.users.tests.factories import EnProfileFactory, RoleFactory, UserFactory
from organizations.tests.factories import OrganizationFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class EnGroupTestCase(APITestCase):
    def setUp(self):
        roles = [
            {"name": "ENO"},
            {"name": "Implementation Manager", "path": "ENO.Implementation Manager"},
            {"name": "Main Implementation Manager", "path": "ENO.Main Implementation Manager"},
            {"name": "Vendor"},
            {"name": "Vendor PM", "path": "Vendor.Vendor PM"},
            {"name": "Project Manager", "path": "ENO.Project Manager"},
            {"name": "Total Project Manager", "path": "ENO.Total Project Manager"},
            {"name": "A S P Manager", "path": "ENO.A S P Manager"},
            {"name": "P S S", "path": "ENO.P S S"},
        ]

        for role in roles:
            RoleFactory(**role)

        self.maxDiff = None

        self.eno_group = Group.objects.get(name="ENO")
        self.user = UserFactory(groups=[self.eno_group])
        self.en_profile = EnProfileFactory(user=self.user)
        self.url = reverse("apiv1:en_groups-list")
        self.all_url = reverse("apiv1:en_groups-all")

        self.organization = OrganizationFactory(name="ENP", domain="enp.localhost")
        self.domain = self.organization.domains.first().name

    # def test_forbidden(self):
    #     """
    #     Disallow delete
    #     """
    #     self.client.force_authenticate(self.user)
    #     response = self.client.delete(self.detail_url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_list(self):
        """
        Successfully list the en_groups using pagination
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, SERVER_NAME=self.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_all(self):
        """
        Successfully list all the en_groups for dropdown
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.all_url, SERVER_NAME=self.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
