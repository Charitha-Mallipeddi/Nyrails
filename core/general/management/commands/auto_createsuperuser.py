import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

User = get_user_model()


class Command(BaseCommand):
    help = "Generate Random Scan Test Data"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Username for the superuser")
        parser.add_argument("--email", type=str, help="Email for the superuser")
        parser.add_argument("--password", type=str, help="Password for the superuser")

    def handle(self, *args, **options):
        username = options.get("username")
        if not username:
            username = os.environ.get("DJANGO_SUPERUSER_USERNAME", None)
        password = options.get("password")
        if not password:
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", None)
        email = options.get("email")
        if not email:
            email = os.environ.get("DJANGO_SUPERUSER_EMAIL", None)

        if not username:
            self.stdout.write(self.style.ERROR("Username is required."))
            return
        if not password:
            self.stdout.write(self.style.WARNING("Password is not provided."))
            self.stdout.write(self.style.WARNING("Generating random password..."))
            password = get_random_string(10)
        if not email:
            self.stdout.write(self.style.ERROR("Email is required."))
            return
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser {username} already exists."),
            )
        else:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser {user.username} created successfully. With password: {password}",
                ),
            )
