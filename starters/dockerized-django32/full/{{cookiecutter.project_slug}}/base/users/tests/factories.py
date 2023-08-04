import factory

TEST_USER_PASSWORD = "password"


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", TEST_USER_PASSWORD)
    name = factory.Faker("name")

    class Meta:
        model = "users.User"
        django_get_or_create = ("name",)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)
