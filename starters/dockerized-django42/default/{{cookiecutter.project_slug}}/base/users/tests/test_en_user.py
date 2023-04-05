from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import override_settings
from eno_a3_django.users.tests.factories import EnProfileFactory, RoleFactory, UserFactory
from organizations.tests.factories import OrganizationFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class EnUserTestCase(APITestCase):
    """
    users.tests.test_en_user.EnUserTestCase.
    """

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
        self.url = reverse("apiv1:en_users-list")

        self.pm_group = Group.objects.get(name="Project Manager")
        self.im_group = Group.objects.get(name="Implementation Manager")

        self.pm_user = UserFactory(
            name="Project Manager User", groups=[self.eno_group, self.pm_group]
        )
        self.pm_en_profile = EnProfileFactory(user=self.pm_user)

        self.im_user = UserFactory(
            name="Implementation Manager User", groups=[self.eno_group, self.im_group]
        )
        self.im_en_profile = EnProfileFactory(user=self.im_user)

        self.detail_url = reverse("apiv1:detailed_en_users-detail", args=(self.pm_user.pk,))
        self.organization = OrganizationFactory(name="ENP", domain="enp.localhost")
        self.domain = self.organization.domains.first().name
        self.by_group_url = reverse("apiv1:en_users-by-group")

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_by_group(self):
        """
        Successfully list all the en_users for dropdown by group name
        """
        self.client.force_authenticate(self.user)
        url = f"{self.by_group_url}?group=Implementation Manager"
        response = self.client.get(url, SERVER_NAME=self.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["users"],
            [
                {
                    "id": self.im_user.pk,
                    "en_profile": {
                        "modified": "{:%Y-%m-%dT%H:%M:%S.%fZ}".format(self.im_en_profile.modified),
                        "modified_by": None,
                        "id": self.im_en_profile.id,
                        "org_unit_short_name": self.im_en_profile.org_unit_short_name,
                        "signum": self.im_en_profile.signum,
                    },
                    "name": self.im_user.name,
                    "first_name": self.im_user.first_name,
                    "last_name": self.im_user.last_name,
                    "username": self.im_user.username,
                    "email": self.im_user.email,
                    "groups": [
                        {"id": self.eno_group.pk, "name": self.eno_group.name},
                        {"id": self.im_group.pk, "name": self.im_group.name},
                    ],
                    "links": {"groups": "groups/"},
                }
            ],
        )

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_list(self):
        """
        Successfully create new user
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, SERVER_NAME=self.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["users"],
            [
                {
                    "id": self.user.pk,
                    "en_profile": {
                        "modified": "{:%Y-%m-%dT%H:%M:%S.%fZ}".format(self.en_profile.modified),
                        "modified_by": None,
                        "id": self.en_profile.id,
                        "org_unit_short_name": self.en_profile.org_unit_short_name,
                        "signum": self.en_profile.signum,
                    },
                    "name": self.user.name,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name,
                    "username": self.user.username,
                    "email": self.user.email,
                    "groups": [],
                },
                {
                    "id": self.pm_user.pk,
                    "en_profile": {
                        "modified": "{:%Y-%m-%dT%H:%M:%S.%fZ}".format(self.pm_en_profile.modified),
                        "modified_by": None,
                        "id": self.pm_en_profile.id,
                        "org_unit_short_name": self.pm_en_profile.org_unit_short_name,
                        "signum": self.pm_en_profile.signum,
                    },
                    "name": self.pm_user.name,
                    "first_name": self.pm_user.first_name,
                    "last_name": self.pm_user.last_name,
                    "username": self.pm_user.username,
                    "email": self.pm_user.email,
                    "groups": [{"id": self.pm_group.pk, "name": self.pm_group.name}],
                    "links": {"groups": "groups/"},
                },
                {
                    "id": self.im_user.pk,
                    "en_profile": {
                        "modified": "{:%Y-%m-%dT%H:%M:%S.%fZ}".format(self.im_en_profile.modified),
                        "modified_by": None,
                        "id": self.im_en_profile.id,
                        "org_unit_short_name": self.im_en_profile.org_unit_short_name,
                        "signum": self.im_en_profile.signum,
                    },
                    "name": self.im_user.name,
                    "first_name": self.im_user.first_name,
                    "last_name": self.im_user.last_name,
                    "username": self.im_user.username,
                    "email": self.im_user.email,
                    "groups": [{"id": self.im_group.pk, "name": self.im_group.name}],
                    "links": {"groups": "groups/"},
                },
            ],
        )

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_save_en_user(self):
        """
        Successfully save en user
        """
        self.client.force_authenticate(self.user)
        data = {
            "name": "Changed User",
            "email": "changed@clientexample.com",
            "en_profile": {"signum": "CHANGED", "org_unit_short_name": "A"},
            "groups": [self.im_group.pk],
        }

        response = self.client.patch(self.detail_url, data, format="json", SERVER_NAME=self.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pm_user.refresh_from_db()
        # need to check for this as this was to ensure that the bug in #725 does not recur
        self.assertTrue(self.im_group in self.pm_user.groups.all())
        self.assertTrue(Group.objects.filter(name="Project Manager").exists())
