import django.contrib.auth.models as auth_models
import factory

TEST_USER_PASSWORD = "password"


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user-{n}")
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", TEST_USER_PASSWORD)
    name = factory.Faker("name")

    class Meta:
        model = "users.User"
        django_get_or_create = ("username",)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class EnProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    signum = factory.Faker("word")
    org_unit_short_name = factory.Faker("word")

    class Meta:
        model = "users.EnProfile"


class VendorUserFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    vendor = factory.SubFactory("vendors.tests.factories.VendorFactory")

    class Meta:
        model = "users.VendorUser"


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = auth_models.Group


class RoleFactory(GroupFactory):
    class Meta:
        model = "users.Role"


class PeopleInSubProjectFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    role = factory.SubFactory(RoleFactory)
    sub_project = factory.SubFactory("service_skus.tests.factories.SubProjectFactory")

    class Meta:
        model = "users.PeopleInSubProject"
