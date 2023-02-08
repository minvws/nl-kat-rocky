from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command
from django_otp.plugins.otp_totp.models import TOTPDevice

from tools.models import (OrganizationMember)

User = get_user_model()


class Command(BaseCommand):
    help = "Helper command for testing and development purposes only"

    def handle(self, **options):
        try:
            first_user = User.objects.get(id=1)
        except:
            print("No first user present")
            return

        member = None
        organization = None
        device = None

        if OrganizationMember.objects.filter(user=first_user).exists():
            member = OrganizationMember.objects.filter(user=first_user).first()
            organization = member.organization

        if TOTPDevice.objects.filter(user=first_user).exists():
            device = TOTPDevice.objects.filter(user=first_user).first()

        call_command("flush", interactive=False)
        call_command("loaddata", "OOI_database_seed.json")
        call_command("setup_dev_account")

        first_user.save()

        if device:
            device.save()
            print("Saved device")

        if member and organization:
            organization.save()
            member.save()

