import json
import os
from django.core.management.base import BaseCommand, CommandError
from core.models import Video

class Command(BaseCommand):
    help = 'Load mock videos from mock_videos.json into the Video model.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='mock_videos.json', help='Path to the mock_videos.json file')
        parser.add_argument('--language', type=str, default='es', help='Language code to use for all videos (default: es)')

    def handle(self, *args, **options):
        file_path = options['file']
        language = options['language']

        if not os.path.exists(file_path):
            raise CommandError(f"File not found: {file_path}")

        with open(file_path, 'r') as f:
            videos = json.load(f)

        created = 0
        Video.objects.all().delete()
        for vid in videos:
            Video.objects.create(
                title=vid['title'],
                language=language,
                vimeo_url=vid['vimeo_url'],
                is_private=vid['is_private']
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created} videos from {file_path}'))
