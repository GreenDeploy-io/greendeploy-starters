from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from eno_a3_django.users.models import EnProfile, Role, User


class Command(BaseCommand):
    help = "Ensures that all users with ericsson.com has a corresponding en profile record"

    def handle(self, *args, **options):
        all_groups = Group.objects.order_by("id").all()
        for group in all_groups:
            try:
                role = Role.objects.get(group_ptr=group)
            except Role.DoesNotExist:
                role = Role(group_ptr=group)
                role.save_base(raw=True)
                role = Role.objects.get(group_ptr=group)
            eno_role = Role.objects.get(pk=1)
            if role.name == "ENO":
                role.path = group.name
            elif group.name == "Vendor":
                role.path = group.name
            else:
                role.path = "ENO." + group.name
                role.under = eno_role
            role.save()
