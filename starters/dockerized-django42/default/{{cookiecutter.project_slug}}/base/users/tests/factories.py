import factory
from django.core.management.utils import get_random_secret_key


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user-{n}")
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", get_random_secret_key())
    name = factory.Faker("name")

    class Meta:
        model = "users.CustomUser"
        django_get_or_create = ("username",)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


