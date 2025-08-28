import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Create a superuser automatically from environment variables if none exists'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if superusers already exist',
        )

    def handle(self, *args, **options):
        # Get environment variables
        admin_username = os.getenv('DJANGO_ADMIN_USER')
        admin_password = os.getenv('DJANGO_ADMIN_PASSWORD')
        admin_email = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@ibitsofphysics.com')

        # Check if environment variables are set
        if not admin_username or not admin_password:
            self.stdout.write(
                self.style.WARNING(
                    'Skipping superuser creation: DJANGO_ADMIN_USER and/or DJANGO_ADMIN_PASSWORD not set'
                )
            )
            return

        # Check if superusers already exist (unless force is used)
        if not options['force'] and User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING(
                    'Superuser already exists. Use --force to create anyway.'
                )
            )
            return

        # Check if user with this username already exists
        if User.objects.filter(username=admin_username).exists():
            if not options['force']:
                self.stdout.write(
                    self.style.WARNING(
                        f'User "{admin_username}" already exists. Use --force to recreate.'
                    )
                )
                UserProfile.objects.update_or_create(
                    user=User.objects.get(username=admin_username),
                    defaults={'has_paid': False}
                )
                return
            else:
                # Delete existing user if force is used
                User.objects.filter(username=admin_username).delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted existing user "{admin_username}"')
                )

        try:
            # Create the superuser
            user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'has_paid': False}
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Superuser "{admin_username}" created successfully!'
                )
            )
            
            # Provide helpful information
            self.stdout.write(
                self.style.HTTP_INFO(
                    f'\nSuperuser Details:\n'
                    f'Username: {admin_username}\n'
                    f'Email: {admin_email}\n'
                    f'Admin URL: /admin/\n'
                )
            )
            
        except Exception as e:
            raise CommandError(f'Error creating superuser: {e}')

        # Show environment variable requirements for reference
        self.stdout.write(
            self.style.HTTP_INFO(
                '\nEnvironment Variables Used:\n'
                '• DJANGO_ADMIN_USER (required)\n'
                '• DJANGO_ADMIN_PASSWORD (required)\n'
                '• DJANGO_ADMIN_EMAIL (optional, defaults to admin@ibitsofphysics.com)\n'
            )
        )
