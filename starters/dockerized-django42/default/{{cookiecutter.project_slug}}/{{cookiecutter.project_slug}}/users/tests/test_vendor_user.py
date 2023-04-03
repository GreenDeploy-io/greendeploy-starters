from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import override_settings
from django.utils import lorem_ipsum
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from eno_a3_django.users.models import VendorUser
from eno_a3_django.users.tests.factories import (
    RoleFactory,
    UserFactory,
    VendorUserFactory,
)
from organizations.tests.factories import OrganizationFactory
from vendors.models import Vendor
from vendors.tests.factories import VendorFactory

User = get_user_model()


class VendorUserTestCase(APITestCase):
    """
    eno_a3_django.users.tests.test_vendor_user.VendorUserTestCase --keepdb
    """

    def setUp(self):
        self.maxDiff = None

        # setup the right roles and people
        roles = [
            {"name": "Vendor"},
            {"name": "Vendor PM", "path": "Vendor.Vendor PM"},
            {"name": "Vendor Admin", "path": "Vendor.Vendor Admin"},
        ]

        for role in roles:
            RoleFactory(**role)

        self.vendor_group = Group.objects.get(name="Vendor")
        self.vendor_pm_group = Group.objects.get(name="Vendor PM")
        self.vendor_admin_group = Group.objects.get(name="Vendor Admin")

        self.user = UserFactory(groups=[self.vendor_group])
        self.organization = OrganizationFactory(name="ENP", domain="enp.localhost")
        self.domain = self.organization.domains.first().name
        self.vendor = VendorFactory(
            supplier_id_number="this_one", organization=self.organization
        )
        self.another_vendor = VendorFactory(
            supplier_id_number="another", organization=self.organization
        )
        self.vendor_user_relation = VendorUserFactory(
            vendor=self.vendor, user=self.user
        )
        self.url = reverse("apiv1:vendor_users-list")
        self.detail_url = reverse("apiv1:vendor_users-detail", args=(self.user.pk,))
        self.update_vendor_pm_detail_url = reverse(
            "apiv1:vendors-vendor-pm", args=(self.vendor.pk,)
        )
        self.update_vendor_admin_detail_url = reverse(
            "apiv1:vendors-vendor-admin", args=(self.vendor.pk,)
        )

    # def test_forbidden(self):
    #     """
    #     Disallow delete
    #     """
    #     self.client.force_authenticate(self.user)
    #     response = self.client.delete(self.detail_url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create(self):
        """
        Successfully create new user
        """
        self.client.force_authenticate(self.user)
        data = {
            "vendor_id": self.vendor.id,
            "name": lorem_ipsum.words(1),
            "first_name": "test",
            "last_name": "test",
            "username": "test",
            "email": lorem_ipsum.words(1) + "@" + lorem_ipsum.words(1) + ".com",
            "groups": [self.vendor_pm_group.id],
        }
        original_status = self.vendor.ready_status

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(VendorUser.objects.count(), 2)
        user = User.objects.last()
        self.assertEqual(user.username, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        vendor = Vendor.objects.get(pk=self.vendor.id)
        self.assertEqual(vendor.vendor_user_count, 2)
        self.assertEqual(vendor.vendor_user_active_count, 2)
        self.vendor.refresh_from_db()
        # no change because vendor needs prices and other stuff to be ready
        self.assertEqual(self.vendor.ready_status, original_status)
        self.assertEqual(self.vendor.ready_status_messages, ["missing prices"])

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_list(self):
        """
        Fetch a list of vendor users
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, SERVER_NAME=self.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["users"],
            [
                {
                    "id": self.user.pk,
                    "name": self.user.name,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name,
                    "username": self.user.username,
                    "email": self.user.email,
                    "vendor_user_profile": {
                        "vendor": {
                            "id": self.vendor.id,
                            "name": self.vendor.name,
                            "display": "{} - ({}) {}".format(
                                self.vendor.supplier_id_number,
                                self.vendor.shortname,
                                self.vendor.name,
                            ),
                            "registered_in_sap": self.vendor.registered_in_sap,
                            "shortname": self.vendor.shortname,
                            "supplier_id_number": self.vendor.supplier_id_number,
                        },
                        "modified": "{:%Y-%m-%dT%H:%M:%S.%fZ}".format(
                            self.vendor_user_relation.modified
                        ),
                        "modified_by": None,
                    },
                }
            ],
        )

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_retrieve(self):
        """
        Fetch a single vendor users
        """
        self.client.force_authenticate(self.user)
        response = self.client.get(self.detail_url, SERVER_NAME=self.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["user"],
            {
                "id": self.user.pk,
                "name": self.user.name,
                "email": self.user.email,
                "groups": [],
                "vendor_user_profile": {
                    "modified": "{:%Y-%m-%dT%H:%M:%S.%fZ}".format(
                        self.vendor_user_relation.modified
                    ),
                    "modified_by": None,
                    "vendor": {
                        "id": self.vendor.id,
                        "name": self.vendor.name,
                        "display": "{} - ({}) {}".format(
                            self.vendor.supplier_id_number,
                            self.vendor.shortname,
                            self.vendor.name,
                        ),
                        "registered_in_sap": self.vendor.registered_in_sap,
                        "shortname": self.vendor.shortname,
                        "supplier_id_number": self.vendor.supplier_id_number,
                    },
                },
            },
        )

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_create_vendor_pm(self):
        """
        Update a single vendor users
        """
        self.client.force_authenticate(self.user)
        data = {
            "name": lorem_ipsum.words(1),
            "email": "test@example.com",
            "username": "test@example.com",
        }

        response = self.client.patch(
            self.update_vendor_pm_detail_url, data, format="json"
        )
        self.assertEqual(User.objects.count(), 2)
        newly_created = User.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": newly_created.pk,
                "name": data["name"],
                "first_name": "",
                "email": data["email"],
                "username": data["username"],
                "groups": [
                    {"id": self.vendor_group.id, "name": "Vendor"},
                    {"id": self.vendor_pm_group.id, "name": "Vendor PM"},
                ],
                "last_name": "",
                "links": {"groups": "groups/"},
            },
        )

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_create_vendor_admin_remove_then_update_in_different_vendor(self):
        """
        Update a single vendor users
        """
        original_user_count = User.objects.count()
        self.client.force_authenticate(self.user)
        data = {
            "name": lorem_ipsum.words(1),
            "email": "vendoradmin@vendor.com",
            "username": "vendoradmin@vendor.com",
        }

        response = self.client.patch(
            self.update_vendor_admin_detail_url, data, format="json"
        )
        self.assertEqual(User.objects.count(), original_user_count + 1)
        newly_created = User.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": newly_created.pk,
                "name": data["name"],
                "first_name": "",
                "email": data["email"],
                "username": data["username"],
                "groups": [
                    {"id": self.vendor_group.id, "name": "Vendor"},
                    {"id": self.vendor_admin_group.id, "name": "Vendor Admin"},
                ],
                "last_name": "",
                "links": {"groups": "groups/"},
            },
        )

        vendoruser = VendorUser.objects.get(user=newly_created)
        # vendor is now this_one
        self.assertEqual(vendoruser.vendor, self.vendor)

        # now delete
        response = self.client.delete(
            self.update_vendor_admin_detail_url, format="json"
        )
        # user remains
        self.assertEqual(User.objects.count(), original_user_count + 1)
        self.update_another_vendor_admin_detail_url = reverse(
            "apiv1:vendors-vendor-admin", args=(self.another_vendor.pk,)
        )

        response = self.client.patch(
            self.update_another_vendor_admin_detail_url, data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # vendor is swapped
        vendoruser = VendorUser.objects.get(user=newly_created)
        self.assertEqual(vendoruser.vendor, self.another_vendor)

    @override_settings(ALLOWED_HOSTS=["*"])
    def test_user_info(self):
        """
        user_info must show vendor and cannot be None
        """
        self.client.force_authenticate(self.user)
        # url = "/api/v1/me/user_info?include[]=groups.name&org"
        url = reverse("apiv1:me-detail", args=("user_info",))

        url += "?include[]=groups.name"

        response = self.client.get(url, format="json", SERVER_NAME=self.domain)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.json()
        self.assertEqual(
            result["groups"], [{"id": self.vendor_group.id, "name": "Vendor"}]
        )

        self.assertEqual(
            result,
            {
                "groups": [{"id": self.vendor_group.id, "name": "Vendor"}],
                "user": {
                    "id": self.user.id,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name,
                    "username": self.user.username,
                    "email": self.user.email,
                    "groups": [self.vendor_group.id],
                    "name": self.user.name,
                    "org": "ENP",
                    "vendor": self.vendor.id,
                    "vendor_display": str(self.vendor),
                    "default_currency": "USD",
                },
            },
        )
