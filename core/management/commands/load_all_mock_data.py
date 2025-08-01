import os
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load all mock data files in the correct order'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading (use with caution)',
        )
        parser.add_argument(
            '--skip-site-content',
            action='store_true',
            help='Skip loading site content',
        )
        parser.add_argument(
            '--skip-videos',
            action='store_true',
            help='Skip loading videos',
        )
        parser.add_argument(
            '--skip-chapter-resources',
            action='store_true',
            help='Skip loading chapter resources',
        )
        parser.add_argument(
            '--skip-superuser',
            action='store_true',
            help='Skip creating superuser',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting to load all mock data...')
        )

        # Step 1: Load site content
        if not options['skip_site_content']:
            self.stdout.write('Loading site content...')
            try:
                call_command('load_mock_site_content')
                self.stdout.write(
                    self.style.SUCCESS('✓ Site content loaded successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error loading site content: {e}')
                )
                return
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Skipping site content loading')
            )

        # Step 2: Load videos
        if not options['skip_videos']:
            self.stdout.write('Loading videos...')
            try:
                call_command('load_mock_videos')
                self.stdout.write(
                    self.style.SUCCESS('✓ Videos loaded successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error loading videos: {e}')
                )
                return
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Skipping videos loading')
            )

        # Step 3: Load chapter resources
        if not options['skip_chapter_resources']:
            self.stdout.write('Loading chapter resources...')
            try:
                clear_flag = '--clear' if options['clear'] else ''
                if clear_flag:
                    call_command('load_mock_chapter_resources', '--clear')
                else:
                    call_command('load_mock_chapter_resources')
                self.stdout.write(
                    self.style.SUCCESS('✓ Chapter resources loaded successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error loading chapter resources: {e}')
                )
                return
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Skipping chapter resources loading')
            )

        # Step 4: Create superuser if environment variables are set
        if not options['skip_superuser']:
            self.stdout.write('Creating superuser from environment variables...')
            try:
                call_command('create_superuser_if_none')
                self.stdout.write(
                    self.style.SUCCESS('✓ Superuser creation completed')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Superuser creation skipped: {e}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Skipping superuser creation')
            )

        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 All mock data loaded successfully!\n'
                'Your IBits of Physics application is ready with sample data.'
            )
        )

        # Provide helpful next steps
        self.stdout.write(
            self.style.HTTP_INFO(
                'Next steps:\n'
                '1. Run: python manage.py runserver\n'
                '2. Visit: http://127.0.0.1:8000\n'
                '3. Access admin: http://127.0.0.1:8000/admin/\n'
                '\nFor deployment, set these environment variables:\n'
                '• DJANGO_ADMIN_USER=your_admin_username\n'
                '• DJANGO_ADMIN_PASSWORD=your_secure_password\n'
                '• DJANGO_ADMIN_EMAIL=your_email@domain.com (optional)\n'
            )
        )
