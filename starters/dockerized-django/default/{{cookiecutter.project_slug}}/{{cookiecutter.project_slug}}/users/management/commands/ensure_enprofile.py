from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from eno_a3_django.users.models import EnProfile, User


class Command(BaseCommand):
    help = "Ensures that all users with ericsson.com has a corresponding en profile record"

    def handle(self, *args, **options):
        users = (
            User.objects.filter(email__contains="ericsson.com")
            .filter(en_profile__isnull=True)
            .all()
        )
        en_group = Group.objects.get(name="ENO")
        for user in users:
            en_profile = EnProfile.objects.create(user=user, org_unit_short_name="MOAIMKBB")
            en_group.user_set.add(user)
