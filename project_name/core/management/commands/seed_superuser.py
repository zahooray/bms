from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            default="admin@test.com",
            help="Superuser email",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="admin123",
            help="Superuser password",
        )
        parser.add_argument(
            "--username",
            type=str,
            default="admin",
            help="Superuser username",
        )
        parser.add_argument(
            "--first-name",
            type=str,
            default="Admin",
            help="Superuser first name",
        )
        parser.add_argument(
            "--last-name",
            type=str,
            default="User",
            help="Superuser last name",
        )

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]
        username = options["username"]
        first_name = options["first_name"]
        last_name = options["last_name"]

        try:
            # Check if superuser exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f"Superuser with email {email} already exists")
                )
                return

            # Create superuser
            User.objects.create_superuser(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Superuser created successfully!\n"
                    f"   Email: {email}\n"
                    f"   Username: {username}\n"
                    f"   Password: {password}\n"
                )
            )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error creating superuser: {str(e)}")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Unexpected error: {str(e)}")
            )
