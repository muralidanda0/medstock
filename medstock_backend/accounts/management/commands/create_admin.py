from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import User


class Command(BaseCommand):
    """
    Creates a superuser automatically from environment variables, but only
    if one with that username doesn't already exist yet. Safe to run on
    every deploy (won't error or duplicate on redeploys), which is exactly
    why we can call this from build.sh instead of needing manual shell access.
    """
    help = 'Creates a superuser from environment variables if one does not already exist'

    def handle(self, *args, **options):
        username = settings.ADMIN_USERNAME
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                'ADMIN_USERNAME or ADMIN_PASSWORD not set — skipping superuser creation.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists — skipping.'))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role=User.Role.ADMIN,
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))